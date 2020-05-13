import React from "react";
import Chip from "@material-ui/core/Chip";
import { useDropzone } from "react-dropzone";
import { useField } from "formik";
import { createStyles, makeStyles, Theme } from "@material-ui/core/styles";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    dropzoneNormal: {
      textAlign: "center",
      padding: "20px",
      border: "3px dashed #eeeeee",
      backgroundColor: "#fafafa",
      color: "#bdbdbd",
    },
    dropzoneError: {
      textAlign: "center",
      padding: "20px",
      border: "3px dashed #e53935",
      backgroundColor: "#fafafa",
      color: "#bdbdbd",
    },
    errorMessage: {
      color: "#e53935",
      marginLeft: "14px",
      marginRight: "14px",
      marginTop: "4px",
      fontSize: "11px",
    },
  })
);

const CustomDropzoneField = (props) => {
  const { onChange, disabled, multiple, value, accept } = props;
  const { name } = props.field;

  const [field, meta] = useField(props);
  const errorText = meta.error && meta.touched ? meta.error : "";

  const classes = useStyles();

  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (files) => onChange(files),
    multiple: multiple,
    accept: accept,
  });

  const file = value;

  if (disabled) {
    return null;
  }

  const dropZoneStyle = errorText[name]
    ? classes.dropzoneError
    : classes.dropzoneNormal;

  return (
    <div>
      <br />
      <div {...getRootProps()} className={dropZoneStyle}>
        <input {...getInputProps()} />
        Upload file here!
      </div>
      <br />
      <div>
        {errorText[name] && (
          <div className={classes.errorMessage}>{errorText[name]}</div>
        )}
        {file && (
          <Chip variant="outlined" color="primary" size="small" label={file} />
        )}
      </div>
    </div>
  );
};

export default CustomDropzoneField;
