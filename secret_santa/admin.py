from django.contrib import admin
from .models import Game, Patricipants, Givers
from .forms import PatricipantsForm, GiversForm


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_game', 'creators_id', 'cost_of_the_gift',
                    'start_of_registration', 'end_of_registration', 'departure_date',
                    'link_to_the_game'
                    )
    search_fields = ('name_of_game', 'start_of_registration', 'cost_of_the_gift')
    list_editable = ('cost_of_the_gift', 'start_of_registration', 'end_of_registration', 'departure_date')
    list_filter = ('cost_of_the_gift',)


@admin.register(Patricipants)
class PatricipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'id_user', 'name',
                    'e_mail', 'interests', 'letter_to_santa'
                    )
    search_fields = ('game',)
    list_filter = ('game',)
    form = PatricipantsForm


@admin.register(Givers)
class GiversAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'givers', 'recipient'
                    )
    search_fields = ('game',)
    list_filter = ('game',)
    form = GiversForm
