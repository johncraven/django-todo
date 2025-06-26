// #region COMMON UTILITIES

// get CSRF token
function getCSRFTokenFromMeta() {
    return document.querySelector('meta[name="csrf-token"]').content
}

// handle a modal
const modal = document.querySelector("#delete-modal")
const btnConfirmDelete = document.querySelector("#confirmDelete")
const btnCancelDelete = document.querySelector("#cancelDelete")

function hideModal() {
    modal.classList.add("hidden")
}

function showModal() {
    modal.classList.remove("hidden")
}

// the Escape key should close the modal at any time
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        hideModal()
    }
})

// clicking the modal's cancel button should also close the modal
btnCancelDelete.addEventListener("click", (event) => {
    hideModal()
})

let deleteHandler = null;
let taskId = null;

// #endregion COMMON UTILITIES


// show/hide nav items at small screen sizes
document.querySelector("#navToggle").addEventListener("click", (event) => {
    document.querySelector(".navlink-list").classList.toggle("showNav")
})

// This will control AJAX deleting TASKS on the Homepage
document.querySelectorAll("[id^='task-delete']").forEach(button => {
    button.addEventListener("click", (event) => {
        showModal()
        if (deleteHandler) {
            btnConfirmDelete.removeEventListener("click", deleteHandler)
        }

        taskId = event.currentTarget.dataset.taskPk
        console.log('Setting taskId to:', taskId) // Debug line

        deleteHandler = async function (event) {
            console.log('Confirming delete for taskId:', taskId)

            // Delete the task 
            const response = await fetch(
                "/task/" + taskId + "/delete/",
                {
                    method: "POST",
                    headers: {
                        'Content-Type': "application/json",
                        'X-CSRFToken': getCSRFTokenFromMeta(),
                    }
                }
            ).then(response => {
                if (response.ok) {
                    console.log("Task deleted successfully")
                    hideModal()
                    let taskItem = document.querySelector("#task-" + taskId).remove()
                } else {
                    console.error("Failed to delete the task")
                }
            })
                .catch(error => {
                    console.error('Error: ', error)
                })
        }
        btnConfirmDelete.addEventListener("click", deleteHandler)
    })
})

// This will control FORM deleting the TASK on the DETAIL VIEW
document.querySelectorAll("#task-detail-delete-button").forEach(button => {
    button.addEventListener("click", (event) => {
        showModal()
        event.preventDefault()

        if (deleteHandler) {
            btnConfirmDelete.removeEventListener("click", deleteHandler)
        }

        taskId = event.currentTarget.dataset.taskPk
        console.log('Setting taskId of the DETAIL VIEW to:', taskId) // Debug line
        let form = document.querySelector("#task-detail-delete-form")
        deleteHandler = function (event) {
            console.log('Confirming delete for DETAIL VIEW taskId:', taskId)
            form.submit()
        }
        btnConfirmDelete.addEventListener("click", deleteHandler)
    })
})

// This will control AJAX deleting the COMMENT on the DETAIL VIEW
document.querySelectorAll("[id^='comment-delete']").forEach(button => {
    button.addEventListener("click", (event) => {
        showModal()
        if (deleteHandler) {
            btnConfirmDelete.removeEventListener("click", deleteHandler)
        }

        commentPk = event.currentTarget.dataset.commentPk
        console.log('Setting commentPk to:', commentPk) // Debug line

        deleteHandler = async function (event) {
            console.log('Confirming delete for commentPk:', commentPk)

            // Delete the task 
            const response = await fetch(
                "/comment/" + commentPk + "/delete/",
                {
                    method: "POST",
                    headers: {
                        'Content-Type': "application/json",
                        'X-CSRFToken': getCSRFTokenFromMeta(),
                    }
                }
            ).then(response => {
                if (response.ok) {
                    console.log("Task deleted successfully")
                    hideModal()

                    // Remove the parent comment list item from the comment list
                    // to match the changes made on the server
                    document.querySelector("#comment-" + commentPk).remove()
                } else {
                    console.error("Failed to delete the task")
                }
            })
                .catch(error => {
                    console.error('Error: ', error)
                })
        }
        btnConfirmDelete.addEventListener("click", deleteHandler)
    })
})

// Task toggle AJAX request
document.querySelectorAll("[id^=toggle-task-]").forEach(button => {
    let taskPk = button.dataset.taskPk
    let isComplete
    button.addEventListener("click", (event) => {
        isComplete != button.classList.contains("checked")
        fetch("/api/task/" + taskPk + "/update_complete",
            {
                method: "PATCH",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFTokenFromMeta()
                },
                body: {
                    "pk": taskPk,
                    "is_complete": isComplete
                }
            }
        ).then(response => {
            if (response.ok) {
                console.log("Updated status for " + taskPk);
                button.classList.toggle("checked");
            } else {
                console.log("Error updating task" + taskPk)
            }
        }).catch(error => {
            console.log('Network Error: ', error)
        })


    })
})