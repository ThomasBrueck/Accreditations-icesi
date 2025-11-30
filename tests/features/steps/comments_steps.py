from behave import when, then
from tests.pages.comments_page import CommentsPage

@when('I navigate to the factor comments creation page')
def step_when_navigate_to_comments_creation(context):
    context.comments_page.navigate_to_comments_creation()

@when('I create a new comment')
def step_when_create_comment(context):
    context.comment_title = "Test Comment"
    context.comment_content = "This is a test comment content."
    context.comments_page.create_comment(context.comment_title, context.comment_content)
    context.comment_id = context.comments_page.get_last_comment_id()

@when('I navigate to the edit page for the comment')
def step_when_navigate_to_edit_comment(context):
    context.comments_page.navigate_to_edit_comment(context.comment_id)

@when('I update the comment')
def step_when_update_comment(context):
    updated_title = "Updated Test Comment"
    updated_content = "This is updated comment content."
    context.comments_page.update_comment(updated_title, updated_content)

@when('I delete the comment as the author')
def step_when_delete_comment_author(context):
    context.comments_page.delete_comment(context.comment_id)

@when('I attempt to delete the comment')
def step_when_attempt_delete_comment(context):
    context.comments_page.attempt_delete_comment(context.comment_id)

@when('I navigate to the comment review page')
def step_when_navigate_to_review_page(context):
    context.comments_page.navigate_to_review_page(context.comment_id)

@when('I approve the comment')
def step_when_approve_comment(context):
    context.comments_page.approve_comment()

@when('I disapprove the comment with justification')
def step_when_disapprove_comment(context):
    context.justification = "Inappropriate content."
    context.comments_page.disapprove_comment(context.justification)

@when('I navigate to the comment justification page')
def step_when_navigate_to_justification_page(context):
    context.comments_page.navigate_to_justification_page(context.comment_id)

@then('I should see a success message for comment creation')
def step_then_verify_creation_success(context):
    assert context.comments_page.verify_success_message("Comentario creado exitosamente"), "Creation success message not displayed"

@then('the comment should appear with pending status')
def step_then_verify_comment_pending(context):
    comments = context.comments_page.get_comments()
    found = False
    for comment in comments:
        if context.comment_title in comment["title"] and "pending" in comment["status"].lower():
            found = True
            break
    assert found, "Comment with pending status not found"

@then('I should see a success message for comment update')
def step_then_verify_update_success(context):
    assert context.comments_page.verify_success_message("Comentario actualizado exitosamente"), "Update success message not displayed"

@then('the comment should show the updated content')
def step_then_verify_updated_content(context):
    comments = context.comments_page.get_comments()
    found = False
    for comment in comments:
        if "Updated Test Comment" in comment["title"]:
            found = True
            break
    assert found, "Updated comment not found"

@then('I should see a success message for comment deletion')
def step_then_verify_deletion_success(context):
    assert context.comments_page.verify_success_message("Comentario eliminado exitosamente"), "Deletion success message not displayed"

@then('the comment should no longer appear')
def step_then_verify_comment_deleted(context):
    comments = context.comments_page.get_comments()
    found = False
    for comment in comments:
        if context.comment_title in comment["title"]:
            found = True
            break
    assert not found, "Deleted comment still appears"

@then('I should see an error message for unauthorized deletion')
def step_then_verify_unauthorized_error(context):
    assert context.comments_page.verify_error_message("No tienes permiso para eliminar este comentario"), "Unauthorized deletion error message not displayed"

@then('I should see a success message for comment approval')
def step_then_verify_approval_success(context):
    assert context.comments_page.verify_success_message("Comment approved successfully"), "Approval success message not displayed"

@then('the comment should have approved status')
def step_then_verify_approved_status(context):
    comments = context.comments_page.get_comments()
    found = False
    for comment in comments:
        if context.comment_title in comment["title"] and "approved" in comment["status"].lower():
            found = True
            break
    assert found, "Comment with approved status not found"

@then('I should see a success message for comment disapproval')
def step_then_verify_disapproval_success(context):
    assert context.comments_page.verify_success_message("Comment disapproved successfully"), "Disapproval success message not displayed"

@then('the comment should have not approved status')
def step_then_verify_not_approved_status(context):
    comments = context.comments_page.get_comments()
    found = False
    for comment in comments:
        if context.comment_title in comment["title"] and "not_approved" in comment["status"].lower():
            found = True
            break
    assert found, "Comment with not approved status not found"

@then('I should see the justification text')
def step_then_verify_justification(context):
    assert context.comments_page.verify_justification(context.justification), "Justification text not displayed"