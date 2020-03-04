from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View
from wrw.utils import isUserLoggedIn, calcScore
from wrw.models import Symptom, User, Factor, UserSingleSymptomSeverity
from plotly.offline import plot
import plotly.graph_objects as go
from datetime import datetime
import colorlover


class FactorPage(View):
    template_name = 'pages/factor.html'

    def initVariables(self, symptom, factor):
        self.users = []
        self.scores = []

        for user in User.objects.all():
            severities = user.getSymptomSeverities(symptom, factor)

            if not severities:
                continue

            score = calcScore(severities)

            self.scores.append(score)
            self.users.append(user)

    def getUsers(self):
        return self.users

    def getScores(self):
        return self.scores

    def getStatisticsChart(self, symptom, factor):
        fig = go.Figure()

        width = [0.5 for i in range(5)]

        max_value = 0
        y_values = [0, 0, 0, 0, 0]
        x_values = ['|-100 ~ -61|', '|-60 ~ -21|',
                    '|-20 ~ 20|', '|21 ~ 60|', '|61 ~ 100|']

        scores = self.getScores()
        for score in scores:
            if score < -60:
                y_values[0] += 1
            elif score < -20:
                y_values[1] += 1
            elif score <= 20:
                y_values[2] += 1
            elif score <= 60:
                y_values[3] += 1
            else:
                y_values[4] += 1

        max_value = max(y_values+[max_value])
        max_value += 3 if max_value % 2 else 2

        fig.add_trace(
            go.Bar(
                x=x_values,
                y=[round(y_value/len(scores), 2) for y_value in y_values],
                text=['%s User%s' % (y_value, 's' if y_value > 1 else '')
                      for y_value in y_values],
                textposition='auto',
                name='%s toal User%s' % (
                    len(scores), 's' if len(scores) > 1 else ''),
                hoverinfo='skip', width=width, marker_color='#8BC8DB'))

        fig.add_layout_image(
            dict(
                source="/static/images/MiserableFace.png",
                xref="paper", yref="paper",
                x=0.08, y=-0.15,
                sizex=0.2, sizey=0.2
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/SadFace.png",
                xref="paper", yref="paper",
                x=0.28, y=-0.15,
                sizex=0.2, sizey=0.2
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/NeutralFace.png",
                xref="paper", yref="paper",
                x=0.48, y=-0.15,
                sizex=0.2, sizey=0.2
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/HappyFace.png",
                xref="paper", yref="paper",
                x=0.68, y=-0.15,
                sizex=0.2, sizey=0.2
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/EcstaticFace.png",
                xref="paper", yref="paper",
                x=0.88, y=-0.15,
                sizex=0.2, sizey=0.2
            ))

        fig.update_layout(height=300, margin=dict(b=100, t=50, r=20, l=20), showlegend=True,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          title=dict(
                              text="Effectiveness as Rated by Users", x=0.5))

        fig.update_xaxes(showticklabels=True, showgrid=False, zeroline=True,
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)',
                         fixedrange=True, title_text='Users of %s for %s' % (factor.title, symptom.name), title_standoff=45, tickfont_size=10)
        fig.update_yaxes(showticklabels=True, showgrid=False, zeroline=True,
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True,
                         autorange=False, tickvals=[round(val*20/100, 2) for val in range(6)], tickformat='%', range=[0, 1], title_text='% of Users')

        plot_div = plot(fig, output_type='div', include_plotlyjs=False,
                        config=dict(displayModeBar=False))

        return plot_div

    def getTimelineChart(self, user, symptom, factor):
        fig = go.Figure()

        usss_list = UserSingleSymptomSeverity.objects.filter(
            symptom=symptom, user_symptom_severities__user=user).exclude(selected_level__isnull=True).order_by('user_symptom_severities__created_at')

        item_list = [dict(
            title=usss.getTitle(),
            description=usss.getDescription(),
            severity=usss.getLevelNum()-1,
            created_at=usss.getCreatedAt()
        ) for usss in usss_list]

        [started_at, ended_at] = user.getFactorStartAndEndDates(factor)
        fig.add_shape(
            x0=started_at, x1=ended_at, y0=0, y1=1, line=dict(width=0),
            type="rect", xref="x", yref="paper", opacity=0.2, fillcolor="yellow")

        line_colors = ['rgba(99, 110, 250, 0)'] * len(item_list)
        fig.add_trace(
            go.Scatter(x=[item['created_at'] for item in item_list],
                       y=[item['severity']
                          for item in item_list],
                       hoverinfo='text',
                       hovertext=[item['title']
                                  for item in item_list],
                       mode='lines+markers',
                       marker=dict(size=[10] * len(item_list), opacity=1,
                                   line=dict(width=12, color=line_colors)),
                       customdata=item_list,
                       name=symptom.name))

        fig.add_layout_image(
            dict(
                source="/static/images/MiserableFace.png",
                xref="paper", yref="paper",
                x=-0.06, y=0.9,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/SadFace.png",
                xref="paper", yref="paper",
                x=-0.06, y=0.7,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/NeutralFace.png",
                xref="paper", yref="paper",
                x=-0.06, y=0.5,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/HappyFace.png",
                xref="paper", yref="paper",
                x=-0.06, y=0.3,
                sizex=0.15, sizey=0.15
            ))
        fig.add_layout_image(
            dict(
                source="/static/images/EcstaticFace.png",
                xref="paper", yref="paper",
                x=-0.06, y=0.1,
                sizex=0.15, sizey=0.15
            ))

        fig.update_layout(height=200, margin=dict(b=20, t=20, r=180, l=60), showlegend=False,
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', hovermode='closest')
        fig.update_xaxes(showticklabels=True, showgrid=False, zeroline=True, ticks="inside",
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True, range=[item_list[0]['created_at'], datetime.today()])
        fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=True,
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True, range=[0, 5])

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

        symptom_id = kwargs['symptom_id'] if 'symptom_id' in kwargs else None
        factor_id = kwargs['factor_id'] if 'factor_id' in kwargs else None

        if symptom_id is None or factor_id is None:
            return HttpResponse('Provided Parameter is invalid.')

        symptom = Symptom.objects.get(id=symptom_id)
        factor = Factor.objects.get(id=factor_id)

        # init variables (scores, users) with symptom, factor
        self.initVariables(symptom, factor)

        statisctics_charts = self.getStatisticsChart(symptom, factor)

        user_timelines = user_timelines = [dict(
            user=dict(
                name=user.first_name + ' ' + user.last_name,
                sex='M' if user.gender == 'male' else 'F',
                age=datetime.today().year-user.birth_year
            ),
            chart=self.getTimelineChart(user, symptom, factor)
        ) for user in self.getUsers()]

        return render(request, self.template_name, dict(
            symptom=symptom,
            factor=factor,
            statisctics_charts=statisctics_charts,
            user_timelines=user_timelines
        ))
