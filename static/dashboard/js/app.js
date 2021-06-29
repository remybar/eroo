//========================================================
// FUNCTIONS
//========================================================

function handleErrors(response) {
  return response.json().then(json => {
    return response.ok ? json : Promise.reject(json)
  });
}

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function addMessage(kind, msg) {
  let messageContainer = document.getElementById("msg-area")
  let msgDiv = document.createElement("div");
  msgDiv.id = `alert_${uuidv4()}`
  msgDiv.className = `alert alert-${kind} alert-dismissible fade show`;
  msgDiv.role = "alert";
  msgDiv.innerHTML = `
    ${msg}
    <button type="button" class="btn-sm btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  messageContainer.appendChild(msgDiv);
  setTimeout(function () { 
      div = document.getElementById(msgDiv.id);
      div.remove();
    },
    5000
  );
}

function deleteWebsite(action_url, csrftoken) {
  const request = new Request(action_url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrftoken,
    },
  });

  fetch(request)
  .then(handleErrors)
  .then((data) => {
    // remove the website in the table
    let el = document.getElementById(`website_${data.key}`);
    el.remove();

    // if the table is empty, hide it
    let tableContainer = document.getElementById("websites-table-container");
    let table = document.getElementById("websites-table");
    
    if (table.rows.length <= 1) {
      tableContainer.style.display = "none";
    }

    addMessage("success", "Votre site web a été supprimé!");
  })
  .catch((data) => {
    addMessage("danger", `${data.error}`.replace("Error: ", ""));
  });
}


function generateWebsite(action_url, csrftoken, rental_url) {
  let formData = new FormData();
  formData.append('rental_url', rental_url);

  const request = new Request(action_url, {
    method: "POST",
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrftoken,
    },
    body: formData,
  });

  // set the button state to 'in progress' + lock it
  let generateBtn = document.getElementById("generate-btn")
  let origInnerHTML = generateBtn.innerHTML;

  generateBtn.disabled = true;
  generateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

  fetch(request)
  .then(handleErrors)
  .then((data) => {
    // refresh the table
    let tableContainer = document.getElementById("websites-table-container");
    let table = document.getElementById("websites-table");
    let tbody = table.getElementsByTagName('tbody')[0];
    
    newRow = tbody.insertRow()
    newRow.setAttribute("id", `ẁebsite_${data.key}`);
    newRow.innerHTML = `
      <td class="border-0"><a target="_blank" href='${data.url}'>${data.name}</a></td>
      <td class="border-0">${data.key}</td>
      <td class="border-0">${data.generated_date}</td>
      <td class="border-0">
          <a data-url='${data.delete_url}' class='website-delete-btn text-tertiary'>
            <span class="fas fa-trash-alt me-2"></span>
            Supprimer
          </a>
      </td>
    `;
    if (table.rows.length > 1) {
      tableContainer.style.display = "block";
    }

    addMessage("success", "Votre site web a été généré avec succès!");

    document.getElementById("id_rental_url").value = "";
    generateBtn.innerHTML = origInnerHTML;
    generateBtn.disabled = false;
  })
  .catch((data) => {
    console.log(data.error);
    addMessage("danger", `${data.error}`.replace("Error: ", ""));
    document.getElementById("id_rental_url").value = "";
    generateBtn.innerHTML = origInnerHTML;
    generateBtn.disabled = false;
  });
}

//========================================================
// EVENT HANDLERS
//========================================================

document.querySelector("#websites-table").addEventListener("click", (e) => {
  if (e.target && e.target.matches(".website-delete-btn")) {
    e.preventDefault();
    const url = e.target.getAttribute("data-url");
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    deleteWebsite(url, csrftoken);
  }
});

document.querySelector("#generate-btn").addEventListener("click", (e) => {
  e.preventDefault();

  const form = document.querySelector("#generate-form");
  const action_url = form.getAttribute('data-url')
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const rental_url = document.querySelector("#id_rental_url").value;

  generateWebsite(action_url, csrftoken, rental_url);
});
