import React from "react";
import { useField } from "formik";
import { TextField } from "@material-ui/core";
import InputMask from "react-input-mask";

const CustomMaskedInputField = ({
  placeholder,
  variant,
  margin,
  label,
  mask,
  ...props
}) => {
  const [field, meta] = useField(props);
  const errorText = meta.error && meta.touched ? meta.error : "";

  return (
    <InputMask
      mask={mask}
      disabled={false}
      maskChar=" "
      {...field}
      label={label}
    >
      {(innerProp) => (
        <TextField
          {...innerProp}
          fullWidth
          placeholder={placeholder}
          variant={variant}
          margin={margin}
          helperText={errorText}
          error={!!errorText}
        />
      )}
    </InputMask>
  );
};

export default CustomMaskedInputField;
