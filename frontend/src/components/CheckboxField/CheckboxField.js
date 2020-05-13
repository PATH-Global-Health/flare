import React from "react";
import { useField } from "formik";
import Checkbox from "@material-ui/core/Checkbox";
import FormControlLabel from "@material-ui/core/FormControlLabel";

export const CustomCheckboxField = ({ label, disabled, ...props }) => {
  const [field, meta] = useField(props);
  const errorText = meta.error && meta.touched ? meta.error : "";
  return (
    <FormControlLabel
      control={
        <Checkbox
          {...field}
          checked={field.value ? true : false}
          disabled={disabled}
          helperText={errorText}
          error={!!errorText}
        />
      }
      label={label}
    />
  );
};

export default CustomCheckboxField;
