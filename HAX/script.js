function validateForm() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const usernameField = document.getElementById("username");
  const passwordField = document.getElementById("password");

  usernameField.classList.remove("error");
  passwordField.classList.remove("error");

  // Простая проверка (ЗАМЕНИТЬ НА ПРОВЕРКУ НА СЕРВЕРЕ!!!)
  if (username.trim() === "" || password.trim() === "") {
    alert("Пожалуйста, заполните все поля!");
    usernameField.classList.add("error");
    passwordField.classList.add("error");
    return false;
  }

  if (username.length < 5 || password.length < 8) {  // Пример простой проверки длины
    alert("Логин должен быть не короче 5 символов, пароль - не короче 8!");
    usernameField.classList.add("error");
    passwordField.classList.add("error");
    return false;
  }


  // В реальном приложении здесь должна быть проверка на сервере
  // После успешной регистрации перенаправляем на другую страницу
  alert("Регистрация успешна!");
  return false; // Предотвращаем стандартную отправку формы
}