document.addEventListener('DOMContentLoaded', function() {
const payBtn = document.getElementById('pay-button');
const messageBox = document.createElement('div');
messageBox.innerText = 'Недостаточно средств';
messageBox.classList.add('message-box');
payBtn.addEventListener('click', () => {
  document.body.appendChild(messageBox);
  setTimeout(() => {
    messageBox.classList.add('show');
  }, 100);
  setTimeout(() => {
    messageBox.classList.remove('show');
    setTimeout(() => {
      messageBox.remove();
    }, 300);
  }, 4000);
});
});