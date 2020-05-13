const hostURL = () => {
  // const protocol = window.location.protocol;
  // const slashes = protocol.concat("//");
  // return slashes.concat(window.location.hostname);

  const url = window.location.href;
  const arr = url.split("/");
  return arr[0] + "//" + arr[2];
};
export default hostURL;
