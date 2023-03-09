# -*- coding: utf-8 -*-

"""
    Module that contains various statistics types. These functions are loaded
    dynamically. There is database record for each function.

    Functions get_*_by_release return dictionary with structure:
    {
        osh.hub.models.SystemRelease: value
    }
"""

import datetime

from django.db.models import Sum
from kobo.hub.models import Task

from osh.hub.scan.models import Scan, ScanBinding, SystemRelease
from osh.hub.scan.service import (diff_fixed_defects_between_releases,
                                  diff_fixed_defects_in_package,
                                  diff_new_defects_between_releases,
                                  diff_new_defects_in_package)
from osh.hub.stats.utils import stat_function
from osh.hub.waiving.models import (DEFECT_STATES, Defect, Result, ResultGroup,
                                    Waiver)

#######
# SCANS
#######


@stat_function(1, "SCANS")
def get_total_scans():
    """
        Scans count

        Number of all submitted scans.
    """
    return Scan.objects.enabled().target().count()


@stat_function(1, "SCANS")
def get_scans_by_release():
    """
        Scans count

        Number of submitted scans by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Scan.objects.enabled().target().by_release(r).count()
    return result


@stat_function(2, "SCANS")
def get_rebases_count():
    """
        Rebase scans count

        Number of all submitted scans of rebases.
    """
    return Scan.objects.rebases().count()


@stat_function(2, "SCANS")
def get_rebases_count_by_release():
    """
        Rebase scans count

        Number of all submitted scans of rebases by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Scan.objects.rebases().by_release(r).count()
    return result


@stat_function(3, "SCANS")
def get_newpkg_count():
    """
        New package scans count

        Number of scans of new packages.
    """
    return Scan.objects.newpkgs().count()


@stat_function(3, "SCANS")
def get_newpkg_count_by_release():
    """
        New package scans count

        Number of scans of new packages by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Scan.objects.newpkgs().by_release(r).count()
    return result


@stat_function(4, "SCANS")
def get_updates_count():
    """
        Update scans count

        Number of scans of updates.
    """
    return Scan.objects.updates().count()


@stat_function(4, "SCANS")
def get_updates_count_by_release():
    """
        Update scans count

        Number of scans of updates by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Scan.objects.updates().by_release(r).count()
    return result

#####
# LOC
#####


@stat_function(1, "LOC")
def get_total_lines():
    """
        Lines of code scanned

        Number of total lines of code scanned.
    """
    sbs = ScanBinding.objects.filter(scan__enabled=True)
    if not sbs:
        return 0
    else:
        return sbs.aggregate(Sum('result__lines'))['result__lines__sum']


@stat_function(1, "LOC")
def get_lines_by_release():
    """
        Lines of code scanned

        Number of LoC scanned by RHEL release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = ScanBinding.objects.filter(
            scan__enabled=True, scan__tag__release=r.id)\
            .aggregate(Sum('result__lines'))['result__lines__sum']
    return result

#########
# DEFECTS
#########


@stat_function(1, "DEFECTS")
def get_total_fixed_defects():
    """
        Fixed defects

        Number of defects that were marked as 'fixed'.
    """
    return Defect.objects.enabled().fixed().count()


@stat_function(1, "DEFECTS")
def get_fixed_defects_by_release():
    """
        Fixed defects

        Number of fixed defects found by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Defect.objects.enabled().by_release(r).fixed().count()
    return result


@stat_function(2, "DEFECTS")
def get_total_fixed_defects_in_rebases():
    """
        Fixed defects in rebases

        Number of defects that were marked as 'fixed' in rebases.
    """
    return Defect.objects.enabled().rebases().fixed().count()


@stat_function(2, "DEFECTS")
def get_fixed_defects_in_rebases_by_release():
    """
        Fixed defects in rebases

        Number of fixed defects found in rebases by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Defect.objects.enabled().rebases().by_release(r)\
            .fixed().count()
    return result


@stat_function(3, "DEFECTS")
def get_total_fixed_defects_in_updates():
    """
        Fixed defects in updates

        Number of defects that were marked as 'fixed' in updates.
    """
    return Defect.objects.enabled().updates().fixed().count()


@stat_function(3, "DEFECTS")
def get_fixed_defects_in_updates_by_release():
    """
        Fixed defects in updates

        Number of fixed defects found in updates by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Defect.objects.enabled().updates().by_release(r)\
            .fixed().count()
    return result


@stat_function(4, "DEFECTS")
def get_total_new_defects():
    """
        New defects

        Number of newly introduced defects.
    """
    return Defect.objects.filter(state=DEFECT_STATES['NEW'], result_group__result__scanbinding__scan__enabled=True).count()


@stat_function(4, "DEFECTS")
def get_new_defects_by_release():
    """
        New defects

        Number of newly introduced defects by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Defect.objects.filter(
            result_group__result__scanbinding__scan__tag__release=r.id,
            state=DEFECT_STATES['NEW'],
            result_group__result__scanbinding__scan__enabled=True
        ).count()
    return result


@stat_function(5, "DEFECTS")
def get_total_new_defects_in_rebases():
    """
        New defects in rebases

        Number of newly introduced defects in rebases.
    """
    return Defect.objects.enabled().rebases().new().count()


@stat_function(5, "DEFECTS")
def get_new_defects_in_rebases_by_release():
    """
        New defects in rebases

        Number of newly introduced defects in rebases by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Defect.objects.enabled().rebases().by_release(r)\
            .new().count()
    return result


@stat_function(6, "DEFECTS")
def get_total_new_defects_in_updates():
    """
        New defects in updates

        Number of newly introduced defects in updates.
    """
    return Defect.objects.enabled().updates().new().count()


@stat_function(6, "DEFECTS")
def get_new_defects_in_updates_by_release():
    """
        New defects in updates

        Number of newly introduced defects in updates by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Defect.objects.enabled().updates().by_release(r)\
            .new().count()
    return result


@stat_function(7, "DEFECTS")
def get_fixed_defects_in_release():
    """
        Fixed defects in one release

        Number of defects that were fixed between first scan and final one.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.by_release(r).enabled():
            result[r] += diff_fixed_defects_in_package(sb)
    return result


@stat_function(8, "DEFECTS")
def get_eliminated_in_rebases_in_release():
    """
        Eliminated newly introduced defects in rebases

        Number of newly introduced defects in rebases that were fixed \
between first scan and final one.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.by_release(r).rebases().enabled():
            result[r] += diff_new_defects_in_package(sb)
    return result


@stat_function(9, "DEFECTS")
def get_eliminated_in_newpkgs_in_release():
    """
        Eliminated newly introduced defects in new packages

        Number of newly introduced defects in new packages that were fixed \
between first scan and final one.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.by_release(r).newpkgs().enabled():
            result[r] += diff_new_defects_in_package(sb)
    return result


@stat_function(10, "DEFECTS")
def get_eliminated_in_updates_in_release():
    """
        Eliminated newly introduced defects in updates

        Number of newly introduced defects in updates that were fixed \
between first scan and final one.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.by_release(r).updates().enabled():
            result[r] += diff_new_defects_in_package(sb)
    return result


# https://gitlab.cee.redhat.com/covscan/covscan/-/issues/157
@stat_function(11, "DEFECTS")
def get_fixed_defects_in_release():  # noqa: F811
    """
        Fixed defects in one release

        Number of defects that were fixed between first scan and final one.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.by_release(r).enabled():
            result[r] += diff_fixed_defects_in_package(sb)
    return result


@stat_function(12, "DEFECTS")
def get_fixed_defects_between_releases():
    """
        Fixed defects between releases

        Number of defects that were fixed between this release and previous one
    """
    releases = SystemRelease.objects.filter(active=True, systemrelease=False)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.filter(scan__tag__release=r.id,
                                             scan__enabled=True):
            result[r] += diff_fixed_defects_between_releases(sb)
    return result


@stat_function(13, "DEFECTS")
def get_new_defects_between_releases():
    """
        New defects between releases

        Number of newly added defects between this release and previous one
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = 0
        for sb in ScanBinding.objects.filter(scan__tag__release=r.id,
                                             scan__enabled=True):
            result[r] += diff_new_defects_between_releases(sb)
    return result

#########
# WAIVERS
#########


@stat_function(1, "WAIVERS")
def get_total_waivers_submitted():
    """
        Waivers submitted

        Number of waivers submitted. (including invalidated)
    """
    return Waiver.waivers.all().count()


@stat_function(1, "WAIVERS")
def get_waivers_submitted_by_release():
    """
        Waivers submitted

        Number of waivers submitted by release. (including invalidated)
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.filter(
            result_group__result__scanbinding__scan__tag__release=r.id,
        ).count()
    return result


@stat_function(2, "WAIVERS")
def get_total_update_waivers_submitted():
    """
        Waivers submitted for regular updates

        Number of waivers submitted for regular updates.
    """
    return Waiver.waivers.updates().count()


@stat_function(2, "WAIVERS")
def get_total_update_waivers_submitted_by_release():
    """
        Waivers submitted for regular updates

        Number of waivers submitted for updates in this release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.updates().by_release(r).count()
    return result


@stat_function(3, "WAIVERS")
def get_total_rebase_waivers_submitted():
    """
        Waivers submitted for rebases

        Number of waivers submitted for rebases.
    """
    return Waiver.waivers.rebases().count()


@stat_function(3, "WAIVERS")
def get_total_rebase_waivers_submitted_by_release():
    """
        Waivers submitted for rebases

        Number of waivers submitted for rebases in this release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.rebases().by_release(r).count()
    return result


@stat_function(4, "WAIVERS")
def get_total_newpkg_waivers_submitted():
    """
        Waivers submitted for newpkg scans

        Number of waivers submitted for new package scans.
    """
    return Waiver.waivers.newpkgs().count()


@stat_function(4, "WAIVERS")
def get_total_newpkg_waivers_submitted_by_release():
    """
        Waivers submitted for newpkg scans

        Number of waivers submitted for new package scans in this release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.newpkgs().by_release(r).count()
    return result


@stat_function(5, "WAIVERS")
def get_total_missing_waivers():
    """
        Missing waivers

        Number of groups that were not waived, but should have been.
    """
    return ResultGroup.objects.missing_waiver().count()


@stat_function(5, "WAIVERS")
def get_missing_waivers_by_release():
    """
        Missing waivers

        Number of groups that were not waived by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = ResultGroup.objects.missing_waiver().by_release(r).count()
    return result


@stat_function(6, "WAIVERS")
def get_total_missing_waivers_in_rebases():
    """
        Missing waivers in rebases

        Number of groups in rebases that were not waived, but should have been.
    """
    return ResultGroup.objects.missing_waiver().rebases().count()


@stat_function(6, "WAIVERS")
def get_missing_waivers_in_rebases_by_release():
    """
        Missing waivers in rebases

        Number of groups in rebases that were not waived by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = ResultGroup.objects.missing_waiver().rebases().\
            by_release(r).count()
    return result


@stat_function(7, "WAIVERS")
def get_total_missing_waivers_in_newpkgs():
    """
        Missing waivers in new packages

        Number of groups in new package scans that were not waived.
    """
    return ResultGroup.objects.missing_waiver().newpkgs().count()


@stat_function(7, "WAIVERS")
def get_missing_waivers_in_newpkgs_by_release():
    """
        Missing waivers in new packages

        Number of groups in new package scans that were not waived by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = ResultGroup.objects.missing_waiver().newpkgs().\
            by_release(r).count()
    return result


@stat_function(8, "WAIVERS")
def get_total_missing_waivers_in_updates():
    """
        Missing waivers in updates

        Number of groups in updates that were not waived.
    """
    return ResultGroup.objects.missing_waiver().updates().count()


@stat_function(8, "WAIVERS")
def get_missing_waivers_in_updates_by_release():
    """
        Missing waivers in updates

        Number of groups in updates that were not waived.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = ResultGroup.objects.missing_waiver().updates().\
            by_release(r).count()
    return result


@stat_function(9, "WAIVERS")
def get_total_is_a_bug_waivers():
    """
        'is a bug' waivers

        Number of waivers with type IS_A_BUG.
    """
    return Waiver.waivers.is_a_bugs().count()


@stat_function(9, "WAIVERS")
def get_is_a_bug_waivers_by_release():
    """
        'is a bug' waivers

        Number of waivers with type IS_A_BUG by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.is_a_bugs().by_release(r).count()
    return result


@stat_function(10, "WAIVERS")
def get_is_a_bug_waivers_in_rebases_by_release():
    """
        'is a bug' waivers in rebases

        Number of waivers with type IS_A_BUG in rebases by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.is_a_bugs().rebases().by_release(r).count()
    return result


@stat_function(11, "WAIVERS")
def get_is_a_bug_waivers_in_newpkgs_by_release():
    """
        'is a bug' waivers in newpkgs

        Number of waivers with type IS_A_BUG in new packages by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.is_a_bugs().newpkgs().by_release(r).count()
    return result


@stat_function(12, "WAIVERS")
def get_is_a_bug_waivers_in_updates_by_release():
    """
        'is a bug' waivers in updates

        Number of waivers with type IS_A_BUG in updates by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.is_a_bugs().updates().by_release(r).count()
    return result


@stat_function(10, "WAIVERS")
def get_total_not_a_bug_waivers():
    """
        'not a bug' waivers

        Number of waivers with type NOT_A_BUG.
    """
    return Waiver.waivers.not_a_bugs().count()


@stat_function(13, "WAIVERS")
def get_not_a_bug_waivers_by_release():
    """
        'not a bug' waivers

        Number of waivers with type NOT_A_BUG by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.not_a_bugs().by_release(r).count()
    return result


@stat_function(14, "WAIVERS")
def get_not_a_bug_waivers_in_rebases_by_release():
    """
        'not a bug' waivers in rebases

        Number of waivers with type NOT_A_BUG in rebases by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.not_a_bugs().rebases().by_release(r).count()
    return result


@stat_function(15, "WAIVERS")
def get_not_a_bug_waivers_in_newpkgs_by_release():
    """
        'not a bug' waivers in newpkgs

        Number of waivers with type NOT_A_BUG in new packages by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.not_a_bugs().newpkgs().by_release(r).count()
    return result


@stat_function(16, "WAIVERS")
def get_not_a_bug_waivers_in_updates_by_release():
    """
        'not a bug' waivers in updates

        Number of waivers with type NOT_A_BUG in updates by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.not_a_bugs().updates().by_release(r).count()
    return result


@stat_function(11, "WAIVERS")
def get_total_fix_later_waivers():
    """
        'fix later' waivers

        Number of waivers with type FIX_LATER.
    """
    return Waiver.waivers.fix_laters().count()


@stat_function(17, "WAIVERS")
def get_fix_later_waivers_by_release():
    """
        'fix later' waivers

        Number of waivers with type FIX_LATER by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.fix_laters().by_release(r).count()
    return result


@stat_function(18, "WAIVERS")
def get_fix_later_waivers_in_rebases_by_release():
    """
        'fix later' waivers in rebases

        Number of waivers with type FIX_LATER in rebases by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.fix_laters().rebases().by_release(r).count()
    return result


@stat_function(19, "WAIVERS")
def get_fix_later_waivers_in_newpkgs_by_release():
    """
        'fix later' waivers in newpkgs

        Number of waivers with type FIX_LATER in new packages by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.fix_laters().newpkgs().by_release(r).count()
    return result


@stat_function(20, "WAIVERS")
def get_fix_later_waivers_in_updates_by_release():
    """
        'fix later' waivers in updates

        Number of waivers with type FIX_LATER in updates by release.
    """
    releases = SystemRelease.objects.filter(active=True)
    result = {}
    for r in releases:
        result[r] = Waiver.waivers.fix_laters().updates().by_release(r).count()
    return result

######
# TIME
######


@stat_function(1, "TIME")
def get_busy_minutes():
    """
        Busy minutes

        Number of minutes during the system was busy.
    """
    result = datetime.timedelta()
    for t in Task.objects.all():
        try:
            result += t.time
        except TypeError:
            pass
    return result.seconds / 60 + (result.days * 24 * 60)


@stat_function(2, "TIME")
def get_minutes_spent_scanning():
    """
        Scanning minutes

        Number of minutes that system spent scanning.
    """
    result = Result.objects.all()
    if not result:
        return 0
    else:
        return result.aggregate(
            Sum('scanning_time'))['scanning_time__sum'] / 60