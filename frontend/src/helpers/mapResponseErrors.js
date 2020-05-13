const mapResponseErrors = (data) => {
  let errors = {};
  for (var property in data) {
    if (data.hasOwnProperty(property)) {
      errors[property] = data[property][0];
    }
  }
  return errors;
};

export default mapResponseErrors;
