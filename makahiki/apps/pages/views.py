"""
main views module to render pages.
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import importlib
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from apps.managers.challenge_mgr import challenge_mgr
from apps.managers.resource_mgr import resource_mgr


@never_cache
def root_index(request):
    """
    hanlde the landing page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse("home_index"))
    return HttpResponseRedirect(reverse("landing", args=()))


@never_cache
@login_required
def index(request):
    """
    handle dynamically lay-outed pages defined in page_settings.
    """
    page_name = request.path[1:][:-1]
    view_objects = {}

    if page_name != "home":
        page_info = challenge_mgr.page_info(request.user, page_name)
        if not page_info:
            raise Http404
        elif not page_info.is_unlock:
            return HttpResponseForbidden('<h1>Permission denied</h1>')

        # get the view_objects
        is_page_defined = supply_view_objects(request, page_name, view_objects)

        if not is_page_defined:
            raise Http404

    # sets the active page
    view_objects['active'] = page_name

    # get user resource rank and usage
    energy_rank_info = resource_mgr.resource_team_rank_info(request.user.get_profile().team,
                                                            "energy")
    view_objects["energy_rank_info"] = energy_rank_info
    water_rank_info = resource_mgr.resource_team_rank_info(request.user.get_profile().team,
                                                           "water")
    view_objects["water_rank_info"] = water_rank_info

    return render_to_response("%s.html" % page_name, {
        "view_objects": view_objects,
        }, context_instance=RequestContext(request))


def supply_view_objects(request, page_name, view_objects):
    """ Returns view_objects supplied widgets defined in PageSettings. """

    page_settings = challenge_mgr.page_settings(page_name)
    if not page_settings:
        return False

    view_objects['widget_templates'] = []
    for page_setting in page_settings:
        widget = page_setting.widget
        view_module_name = 'apps.widgets.' + widget + '.views'
        page_views = importlib.import_module(view_module_name)
        widget = widget.replace(".", "__")
        view_objects[widget] = page_views.supply(request, page_name)

        widget_template = "widgets/" + \
                          page_setting.widget.replace(".", "/") + \
                          "/templates/index.html"
        view_objects['widget_templates'].append(widget_template)

    return True


def _get_widget_css(view_objects):
    """
    Returns the contents of the available widget css file
    """
    widget_css = ""
    for widget in view_objects.keys():
        widget_css_file = "%s/apps/widgets/%s/templates/css.css" % (
        settings.PROJECT_ROOT, widget)
        try:
            infile = open(widget_css_file)
            widget_css += infile.read() + "\n"
        except IOError:
            pass
    return widget_css
