const cleanLocalStorage = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("expirationDate");
  localStorage.removeItem("userId");
  localStorage.removeItem("userName");
  localStorage.removeItem("email");
};

export default cleanLocalStorage;
