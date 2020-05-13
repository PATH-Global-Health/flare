import React from "react";
import { useField } from "formik";
import {
  Select,
  FormControl,
  InputLabel,
  FormHelperText,
} from "@material-ui/core";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    formControl: {
      margin: theme.spacing(0),
      minWidth: 120,
    },
  })
);

const CustomSelectField = ({ variant, margin, label, ...props }) => {
  const [field, meta] = useField(props);
  const errorText = meta.error && meta.touched ? meta.error : "";
  const classes = useStyles();

  const randLabelId = Math.random()
    .toString(36)
    .replace(/[^a-z]+/g, "")
    .substr(0, 9);

  const cleanFields = { ...field };
  cleanFields.value = cleanFields.value === undefined ? "" : cleanFields.value;

  return (
    <FormControl
      variant={variant}
      className={classes.formControl}
      error={!!errorText}
    >
      <InputLabel id={randLabelId}>{label}</InputLabel>
      <Select
        margin={margin}
        {...cleanFields}
        label={label}
        labelId={randLabelId}
      >
        {props.children}
      </Select>
      {!!errorText && <FormHelperText>{errorText}</FormHelperText>}
    </FormControl>
  );
};

export default CustomSelectField;
