from django.contrib import admin
from .models import Game, Patricipants, Givers
# from .forms import UsersForm


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_of_game', 'creators_id', 'cost_of_the_gift',
                    'start_of_registration', 'end_of_registration', 'departure_date',
                    'link_to_the_game'
                    )
    # form = UsersForm


@admin.register(Patricipants)
class PatricipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'id_user', 'name',
                    'e_mail', 'interests', 'letter_to_santa'
                    )


@admin.register(Givers)
class GiversAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'givers', 'recipient'
                    )
