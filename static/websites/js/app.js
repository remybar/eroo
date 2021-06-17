document.querySelector("#generate-btn").addEventListener("click", (event) => {
  event.preventDefault();

  const form = document.querySelector("#generate-form");
  const action_url = form.getAttribute('data-url') || window.location.href
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  let formData = new FormData();
  formData.append('rental_url', document.querySelector("#id_rental_url").value);

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
  // let generateBtn = document.querySelector("#generateBtn")

  fetch(request)
    .then((response) => {
      console.log(response);
      return response.json();
    })
    .then((data) => {
      // reset the button state
      console.log(data);

      if (data.status === "ok") {
        
        // open the URL in a new tab/window
        window.open(data.url, '_blank');

        // TODO: display a success message
        console.log(data.url)

        // TODO: refresh the list

        // TODO: handle the generation limit
      } else {
        // TODO: display the error message
        console.log(data.msg)
      }
    });
});
