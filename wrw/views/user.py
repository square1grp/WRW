from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Symptom, Factor, UserSingleSymptomSeverity, UserIntermittentFactor, UserDailyFactorMeta, UserDailyFactorStart
from wrw.utils import isUserLoggedIn
from datetime import datetime, date, timedelta
from plotly.offline import plot
import plotly.graph_objects as go
import colorlover
from django.core.exceptions import ObjectDoesNotExist


class UserPage(View):
    template_name = 'pages/user.html'

    def getSymptomsScatters(self, user, for_sync=False):
        symptom_updates_list = []
        scatters = []
        created_at_list = []

        for symptom in Symptom.objects.all():
            usss_list = UserSingleSymptomSeverity.objects.filter(
                symptom=symptom, user_symptom_severities__user=user).exclude(selected_level__isnull=True).order_by('user_symptom_severities__created_at')

            symptom_updates_list.append(
                dict(name=str(symptom), data=[dict(
                    title=usss.getTitle(),
                    description=usss.getDescription(),
                    severity=usss.getLevelNum()-1,
                    created_at=usss.getCreatedAt()
                ) for usss in usss_list]))

        colors = colorlover.scales['10']['qual']['Paired']
        colors = ['255, 0, 0'] + [text[4:-2] for text in colors]
        for index, symptom_updates in enumerate(symptom_updates_list):
            item_list = symptom_updates['data']

            if not for_sync:
                line_colors = ['rgba(%s, 0)' % colors[index]] * len(item_list)

                scatters.append(
                    go.Scatter(x=[item['created_at'] for item in item_list],
                               y=[item['severity']
                                  for item in item_list],
                               hoverinfo='text',
                               hovertext=[item['title']
                                          for item in item_list],
                               mode='lines+markers',
                               marker=dict(size=[10] * len(item_list), opacity=1, color='rgb(%s)' % colors[index], line=dict(
                                   width=12, color=line_colors)),
                               line_color='rgb(%s)' % colors[index],
                               customdata=item_list,
                               name=symptom_updates['name']))
            else:
                for item in item_list:
                    if item['created_at'] not in created_at_list:
                        created_at_list.append(item['created_at'])

        return scatters if not for_sync else created_at_list

    def getSymptomsScatterChart(self, user):
        fig = go.Figure()

        for scatter in self.getSymptomsScatters(user):
            fig.add_trace(scatter)

        created_at_list = self.getFactorsScatters(user, True)
        if datetime.today() not in created_at_list:
            created_at_list.append(datetime.today())

        fig.add_trace(go.Scatter(x=created_at_list,
                                 y=[0]*len(created_at_list),
                                 hoverinfo='none',
                                 mode='markers',
                                 marker=dict(size=10, opacity=0, line=dict(width=0))))

        fig.add_layout_image(
            dict(
                source="/static/images/MiserableFace.png",
                xref="paper", yref="paper",
                x=-0.05, y=0.9,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/SadFace.png",
                xref="paper", yref="paper",
                x=-0.05, y=0.7,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/NeutralFace.png",
                xref="paper", yref="paper",
                x=-0.05, y=0.5,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/HappyFace.png",
                xref="paper", yref="paper",
                x=-0.05, y=0.3,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/EcstaticFace.png",
                xref="paper", yref="paper",
                x=-0.05, y=0.1,
                sizex=0.15, sizey=0.15
            ))

        fig.update_layout(height=250, margin=dict(b=20, t=20, r=180, l=60), showlegend=True,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='closest')
        fig.update_xaxes(showticklabels=True, showgrid=False, zeroline=True, ticks="inside",
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True)
        fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=True,
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True, range=[0, 5])

        return plot(fig, output_type='div', include_plotlyjs=False,
                    config=dict(displayModeBar=False))

    def checkActiveUDFMUpdates(self, udfm_updates):
        if len(udfm_updates):
            latest_udfm = udfm_updates[-1]

            latest_date = latest_udfm['created_at'].date()

            today = datetime.today()
            d_days = (today.date() - latest_date).days-1
            d_days_condition = 0 if today.hour < 12 else -1

            if latest_udfm['is_ended']:
                d_days = (latest_udfm['ended_at'].date() - latest_date).days-1
                today = latest_udfm['ended_at'].date()
                d_days_condition = 0

            while d_days > d_days_condition:
                created_at = today-timedelta(days=d_days)
                created_at = '%s 12:00:00' % created_at.strftime(
                    '%m/%d/%Y')
                created_at = datetime.strptime(
                    created_at, '%m/%d/%Y %H:%M:%S')

                udfm_updates.append(dict(
                    title=latest_udfm['title'],
                    description=latest_udfm['description'],
                    severity=latest_udfm['severity'],
                    created_at=created_at,
                    is_ended=False))

                d_days -= 1

            created_at_list = [udfm['created_at'] for udfm in udfm_updates]

            for idx in range(len(created_at_list)-1):
                d_days = (created_at_list[idx+1].date() -
                          created_at_list[idx].date()).days-1

                udfm = udfm_updates[idx]

                while d_days > 0:
                    created_at = created_at_list[idx +
                                                 1].date()-timedelta(days=d_days)
                    created_at = '%s 12:00:00' % created_at.strftime(
                        '%m/%d/%Y')
                    created_at = datetime.strptime(
                        created_at, '%m/%d/%Y %H:%M:%S')

                    udfm_updates.append(dict(
                        title=udfm['title'],
                        description=udfm['description'],
                        severity=udfm['severity'],
                        created_at=created_at,
                        is_ended=False))

                    d_days -= 1

        return sorted(udfm_updates, key=lambda k: k['created_at'])

    def getFactorsScatters(self, user, for_sync=False):
        factor_updates = dict()
        scatters = []
        created_at_list = []

        none_point = dict(
            title=None,
            description=None,
            severity=None,
            created_at=None,
        )

        for factor in Factor.objects.all():
            uif_list = [uif for uif in UserIntermittentFactor.objects.filter(user_factors__user=user, factor=factor).exclude(
                selected_level__isnull=True).order_by('user_factors__created_at')]

            udfs_list = [udfs for udfs in UserDailyFactorStart.objects.filter(
                user=user, factor=factor).order_by('created_at')]

            uf_data_list = uif_list + udfs_list
            uf_data_list.sort(key=lambda x: x.getCreatedAt())

            factor_updates[str(factor)] = []

            for uf_data in uf_data_list:
                if isinstance(uf_data, UserIntermittentFactor):
                    factor_updates[str(factor)] += [dict(
                        title=uf_data.getTitle(),
                        description=uf_data.getDescription(),
                        severity=uf_data.getLevelNum(),
                        created_at=uf_data.getCreatedAt()
                    )]
                elif isinstance(uf_data, UserDailyFactorStart):
                    udfm_list = [udfm for udfm in UserDailyFactorMeta.objects.filter(user_daily_factor_start=uf_data).exclude(
                        selected_level__isnull=True).order_by('created_at')]

                    if not len(udfm_list):
                        continue

                    udfm_updates = [dict(
                        title=udfm.getTitle(),
                        description=udfm.getDescription(),
                        severity=udfm.getLevelNum(),
                        created_at=udfm.getCreatedAt(),
                        is_ended=udfm.isEnded(),
                        ended_at=udfm.getEndedAt()
                    ) for udfm in udfm_list]

                    udfm_updates = self.checkActiveUDFMUpdates(
                        udfm_updates)

                    if len(factor_updates[str(factor)]):
                        factor_updates[str(factor)] += [none_point]

                    factor_updates[str(factor)] += udfm_updates

                    if udfm_list[-1].isEnded() and factor_updates[str(factor)][-1] != none_point:
                        factor_updates[str(factor)] += [none_point]

        colors = colorlover.scales['10']['qual']['Paired']
        colors = ['255, 0, 0'] + [text[4:-2] for text in colors]

        index = 0
        for factor in factor_updates:
            item_list = factor_updates[factor]

            if not for_sync:
                line_colors = ['rgba(%s, 0)' % colors[index]] * len(item_list)

                scatters.append(
                    go.Scatter(x=[item['created_at'] for item in item_list],
                               y=[item['severity'] if not for_sync else -1
                                  for item in item_list],
                               hoverinfo='text',
                               hovertext=[item['title']
                                          for item in item_list],
                               mode='lines+markers',
                               marker=dict(size=[10] * len(item_list), opacity=1, color='rgb(%s)' % colors[index], line=dict(
                                   width=12, color=line_colors)),
                               line_color='rgb(%s)' % colors[index],
                               customdata=item_list,
                               name=factor))
            else:
                for item in item_list:
                    if item['created_at'] not in created_at_list:
                        created_at_list.append(item['created_at'])

            index += 1

        return scatters if not for_sync else created_at_list

    def getFactorsScatterChart(self, user):
        fig = go.Figure()

        for scatter in self.getFactorsScatters(user):
            fig.add_trace(scatter)

        created_at_list = self.getSymptomsScatters(user, True)
        if datetime.today() not in created_at_list:
            created_at_list.append(datetime.today())

        fig.add_trace(go.Scatter(x=created_at_list,
                                 y=[0]*len(created_at_list),
                                 hoverinfo='none',
                                 mode='markers',
                                 marker=dict(size=10, opacity=0, line=dict(width=0))))

        fig.update_layout(height=250, margin=dict(b=20, t=20, r=180, l=60), showlegend=True,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='closest',
                          yaxis=dict(tickvals=[i for i in range(6)]))
        fig.update_xaxes(showticklabels=True, showgrid=False, zeroline=True, ticks="inside",
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True)
        fig.update_yaxes(showticklabels=True, showgrid=False, zeroline=True, title_text='Frequency/Magnitude',
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True, range=[0, 6])

        return plot(fig, output_type='div', include_plotlyjs=False,
                    config=dict(displayModeBar=False))

    def get(self, request, *args, **kwargs):
        user_id = isUserLoggedIn(request)

        if not user_id:
            return HttpResponseRedirect('/')

        try:
            user = User.objects.get(id=user_id)
        except:
            return HttpResponse('No user.')

        user_symptoms = []
        for symptom in Symptom.objects.all():
            try:
                UserSingleSymptomSeverity.objects.filter(
                    user_symptom_severities__user=user, symptom=symptom)

                user_symptoms.append(symptom)
            except ObjectDoesNotExist:
                pass

        symptoms_chart = self.getSymptomsScatterChart(user)
        factors_chart = self.getFactorsScatterChart(user)

        return render(request, self.template_name, dict(
            user=user,
            user_symptoms=user_symptoms,
            symptoms_chart=symptoms_chart,
            factors_chart=factors_chart
        ))
