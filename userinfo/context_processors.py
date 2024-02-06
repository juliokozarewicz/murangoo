from .models import User_info


# Em context_processors.py
def global_context_userinfo(request):

    try:
        # contex dect
        context = {}

        # model query
        query_user_data = User_info.objects.filter(user=request.user).first().name

        # initials name
        initials_user = query_user_data.split()

        # First name
        first_name = list(query_user_data.split())[0]
        first_name = first_name.lower().capitalize()
        context['first_name_global'] = str(first_name)

        if len(initials_user) == 1:

            initials_user = list(initials_user[0])

            initials_user = initials_user[0] + initials_user[1]

        if len(initials_user) > 1:

            first_name = list(initials_user[0])[0]
            last_name = list(initials_user[-1])[0]

            initials_user = first_name + last_name

        else:
            initials_user = '--'

        context['user_initials'] = initials_user

        return context

    except:
        context = {}
        context['user_initials'] = '--'
        return context