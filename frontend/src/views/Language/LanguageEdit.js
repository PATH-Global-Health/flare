import React, { useState, useEffect } from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import { useHistory } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardContent,
  CardActions,
  Divider,
  Grid,
  Button,
  CircularProgress,
  Snackbar,
  Box,
} from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import { TextField } from "../../components";
import { Formik, Field, Form } from "formik";
import * as yup from "yup";
import { useDispatch, useSelector } from "react-redux";
import { fetchLanguage, editLanguage } from "../../store/actions";

const useStyles = makeStyles((theme) => ({
  root: {
    margin: theme.spacing(4),
  },
  saving: {
    color: "#FFF",
    marginRight: "5px",
  },
}));

const validationSchema = yup.object({
  name: yup.string().required().max(10),
  code: yup.string().required().max(4),
});

const LanguageEdit = (props) => {
  const { className, staticContext, ...rest } = props;

  const classes = useStyles();
  let history = useHistory();
  const dispatch = useDispatch();
  const [showError, setShowError] = useState(false);

  //redux
  const { language, loadingLanguage, error } = useSelector((state) => ({
    language: state.language.language,
    loadingLanguages: state.language.loadingLanguages,
    error: state.language.error,
  }));

  useEffect(() => {
    dispatch(fetchLanguage(props.match.params.id, history));
  }, [dispatch]);

  const handleCancel = () => {
    history.push("/language");
  };

  const handleClose = () => {
    setShowError(false);
  };

  return loadingLanguage || language === null ? (
    <Box
      display="flex"
      justifyContent="center"
      m={1}
      p={1}
      bgcolor="background.paper"
      className={classes.message}
    >
      <CircularProgress size={100} thickness={1.5} />
    </Box>
  ) : (
    <React.Fragment>
      <Formik
        validateOnChange={true}
        initialValues={language}
        enableReinitialize={true}
        validationSchema={validationSchema}
        onSubmit={(data, { setSubmitting, setErrors }) => {
          setSubmitting(true);

          dispatch(
            editLanguage(data, props.match.params.id, history, (err) => {
              if (typeof err === "string") {
                setShowError(true);
              } else {
                setErrors(err);
              }
              setSubmitting(false);
            })
          );
        }}
      >
        {({ values, errors, isSubmitting }) => (
          <Card {...rest} className={clsx(classes.root, className)}>
            <Form autoComplete="off">
              <CardHeader subheader="Edit a language" title="Language" />
              <Divider />
              <CardContent>
                <Grid container spacing={3}>
                  <Grid item md={12} xs={12}>
                    <Field
                      placeholder="Name"
                      name="name"
                      type="input"
                      variant="outlined"
                      label="Name"
                      margin="dense"
                      as={TextField}
                    />
                  </Grid>
                  <Grid item md={12} xs={12}>
                    <Field
                      placeholder="Code"
                      name="code"
                      type="input"
                      variant="outlined"
                      label="Code"
                      margin="dense"
                      as={TextField}
                    />
                  </Grid>
                </Grid>
              </CardContent>
              <Divider />
              <CardActions>
                <Button
                  color="primary"
                  variant="contained"
                  type="submit"
                  disabled={isSubmitting}
                >
                  {isSubmitting && (
                    <CircularProgress
                      variant="indeterminate"
                      disableShrink
                      className={classes.saving}
                      size={14}
                      thickness={4}
                    />
                  )}
                  Save
                </Button>
                <Button
                  color="primary"
                  variant="text"
                  onClick={handleCancel}
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
              </CardActions>
            </Form>
          </Card>
        )}
      </Formik>

      <Snackbar open={showError} autoHideDuration={5000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </React.Fragment>
  );
};

LanguageEdit.propTypes = {
  className: PropTypes.string,
};

export default LanguageEdit;
