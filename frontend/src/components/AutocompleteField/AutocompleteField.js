import React from "react";
import Autocomplete from "@material-ui/lab/Autocomplete";
import { TextField } from "@material-ui/core";
import { fieldToTextField } from "formik-material-ui";

const AutocompleteField = ({ textFieldProps, ...props }) => {
  const {
    form: { setTouched, setFieldValue },
  } = props;
  const { error, helperText, ...field } = fieldToTextField(props);
  const { name } = field;

  return (
    <Autocomplete
      {...props}
      {...field}
      onChange={(_, value) => setFieldValue(name, value)}
      onBlur={() => setTouched({ [name]: true })}
      renderInput={(props) => (
        <TextField
          {...props}
          {...textFieldProps}
          helperText={helperText}
          error={error}
        />
      )}
    />
  );
};

export default AutocompleteField;
