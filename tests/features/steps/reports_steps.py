from behave import when, then
from tests.pages.reports_page import ReportsPage

@when('I navigate to the reports page')
def step_when_navigate_to_reports(context):
    context.reports_page = ReportsPage(context.driver)
    context.reports_page.navigate_to_reports()

@when('I apply a filter with an active search')
def step_when_apply_filter(context):
    context.search_term = "ejem"
    context.filter_status = "Activo"
    context.reports_page.apply_filter(context.search_term, context.filter_status)

@then('the results should match both search and filter')
def step_then_verify_results(context):
    reports = context.reports_page.get_reports()
    assert reports, "No reports found"
    for report in reports:
        assert context.search_term.lower() in report["title"].lower(), f"Report '{report['title']}' does not match search '{context.search_term}'"
        assert report["status"].lower() == context.filter_status.lower(), f"Report '{report['title']}' status '{report['status']}' does not match '{context.filter_status}'"

@then('the filter tags should be visible')
def step_then_verify_filter_tags(context):
    assert context.reports_page.verify_filter_tags(context.search_term, context.filter_status), "Filter tags not visible"