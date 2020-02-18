from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from wrw.models import User, Symptom, UserSingleSymptomSeverity
from wrw.utils import isUserLoggedIn
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objects as go
import colorlover


class UserPage(View):
    template_name = 'pages/user.html'

    def getSymptomsScatterChart(self, user):
        fig = go.Figure()

        symptom_updates_list = []

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

            sizes = [10] * len(item_list)

            line_colors = ['rgba(%s, 0)' % colors[index]] * len(item_list)
            fig.add_trace(go.Scatter(x=[item['created_at'] for item in item_list],
                                     y=[item['severity']
                                        for item in item_list],
                                     hoverinfo='text',
                                     hovertext=[item['title']
                                                for item in item_list],
                                     mode='lines+markers',
                                     marker=dict(size=sizes, opacity=1, color='rgb(%s)' % colors[index], line=dict(
                                         width=12, color=line_colors)),
                                     line_color='rgb(%s)' % colors[index],
                                     customdata=item_list,
                                     name=symptom_updates['name']))

        fig.add_trace(go.Scatter(x=[datetime.today()],
                                 y=[0],
                                 hoverinfo='none',
                                 mode='markers',
                                 marker=dict(size=sizes, opacity=0, line=dict(width=0))))

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
        fig.update_xaxes(showticklabels=True, showgrid=False, zeroline=True,
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True)
        fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=True,
                         showline=True, linewidth=5, linecolor='rgba(0,0,0,0.5)', fixedrange=True, autorange=False, range=[0, 5])

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

        symptoms_chart = self.getSymptomsScatterChart(user)

        return render(request, self.template_name, dict(
            user=user,
            symptoms_chart=symptoms_chart
        ))
