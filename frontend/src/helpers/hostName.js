const hostName = () => {
  const url = window.location.href;
  const arr = url.split("/");
  return arr[2];
};
export default hostName;
