//========================================================
// FUNCTIONS
//========================================================

function handleErrors(response) {
  if (!response.ok) {
      throw Error(response.statusText);
  }
  return response;
}

function addMessage(kind, msg) {
  let messageContainer = document.getElementById("msg-area")
  let msgDiv = document.createElement("div");
  msgDiv.className = `alert alert-${kind} alert-dismissible fade show`;
  msgDiv.innerHTML = `
    ${msg}
    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
  `;
  messageContainer.appendChild(msgDiv);
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
  })
  .catch((error) => {
    addMessage("danger", `${error}`.replace("Error: ", ""));
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

      // TODO: display a success message

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

      // TODO: handle the generation limit

      document.getElementById("id_rental_url").value = "";
      generateBtn.innerHTML = origInnerHTML;
      generateBtn.disabled = false;
    })
    .catch((error) => {
      console.log(error);
      addMessage("danger", `${error}`.replace("Error: ", ""));
      document.getElementById("id_rental_url").value = "";
      generateBtn.innerHTML = origInnerHTML;
      generateBtn.disabled = false;
    });
}

//========================================================
// EVENT HANDLERS
//========================================================

document.querySelector("#websites-table").addEventListener("click", (e) => {
  e.preventDefault();

  if (e.target && e.target.matches(".website-delete-btn")) {
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
