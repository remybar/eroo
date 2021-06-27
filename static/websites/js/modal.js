const modal = document.querySelector('.modal')
const btn = document.querySelector('#btn-modal')
const btnMenu = document.querySelector('#btn-modal-menu')
const close = document.querySelector('#btn-modal-close')
  
btn.addEventListener('click', function () {
    modal.classList.toggle("is-active")
})

btnMenu.addEventListener('click', function () {
    modal.classList.toggle("is-active")
})

close.addEventListener('click', function () {
    modal.classList.toggle("is-active")
})
 
window.addEventListener('click', function (event) {
    if (event.target.className === 'modal-background') {
        modal.classList.toggle("is-active")
    }
})
