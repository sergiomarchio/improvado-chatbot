
function processMessageResponse(data) {
    hideMessageSpinner();

    console.log(data);

    if ('message' in data) {
        addNewMessage(data['message']);
    } else {
        addErrorMessage();
    }

}


function addNewMessage(message) {
    let newMessage = document.createElement("div");
    newMessage.innerHTML = message['content'];

    newMessage.classList.add("message")
    newMessage.classList.add(message['sender'])

    chatHistory.insertBefore(newMessage, messageEnd);

    messageEnd.scrollIntoView();
}

function addErrorMessage() {
    console.log("EEEERRRRORROROROORORORRRRR!!!!!!");
}

function hideMessageSpinner() {
    messageEnd.classList.add("hidden");
}

function showMessageSpinner() {
    messageEnd.classList.remove("hidden");
    messageEnd.scrollIntoView();
}

function post(url, body, action, errorAction) {
    fetch(url, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: body
    })
    .then(response => response.json())
    .then(data => action(data))
    .catch((error) => errorAction(error));
}

function messageSubmit(event) {
    // prevent page reload
    if (event) {
        event.preventDefault();
    }

    const userMessage = {
        sender: "user",
        content: userMessageField.value
    }
    addNewMessage(userMessage);

    let formData = new FormData(chatForm)

    userMessageField.value = "";
    userMessageField.focus();

    showMessageSpinner();
    post("process_message/", formData, processMessageResponse,
        (error) => {
            hideMessageSpinner();
            addErrorMessage();
        });
}


const csrftoken = getCookie('csrftoken');

const chatHistory = document.getElementById("chat-history");
const messageEnd = document.getElementById("end-marker");
const chatForm = document.getElementById("chat-form");
const userMessageField = document.getElementById("input-field");

chatForm.addEventListener("submit", messageSubmit);


window.onload = function() {
    messageEnd.scrollIntoView();
    userMessageField.focus();
}
