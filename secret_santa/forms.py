from django import forms
from .models import Game, Patricipants, Givers


# class GameForm(forms.ModelForm):
#
#     class Meta:
#         model = Game
#         fields = (
#             'name_of_game',
#             'creators_id',
#             'cost_of_the_gift',
#             'start_of_registration',
#             'end_of_registration'
#             'departure_date',
#             'link_to_the_game',
#         )
#         widgets = {
#
#         }


class PatricipantsForm(forms.ModelForm):

    class Meta:
        model = Patricipants
        fields = (
            'game',
            'id_user',
            'name',
            'e_mail',
            'interests',
            'letter_to_santa',
        )
        widgets = {
            'name': forms.TextInput
        }


class GiversForm(forms.ModelForm):

    class Meta:
        model = Givers
        fields = (
            'game',
            'givers',
            'recipient',
        )
        widgets = {
            'recipient': forms.TextInput
        }
