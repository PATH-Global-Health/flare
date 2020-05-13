import React, { useState } from "react";
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
  MenuItem,
} from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import { MaskedInputField, SelectField } from "../../components";
import { Formik, Field, Form } from "formik";
import * as yup from "yup";
import { useDispatch, useSelector } from "react-redux";
import { addSubscriber } from "../../store/actions";

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
  phone_number: yup
    .string()
    .required()
    .matches(/^[+]{1}[1-9]{1}\d{2}-{1}\d{3}-{1}\d{6}$/, {
      message: "Incorrect phone number format",
      excludeEmptyString: true,
    }),
  language: yup.number().required(),
});

const SubscriberAdd = (props) => {
  const { className, staticContext, ...rest } = props;

  const phoneMask = "+999-999-999999";

  const classes = useStyles();
  const history = useHistory();
  const dispatch = useDispatch();
  const { error, lookup } = useSelector((state) => ({
    error: state.subscriber.error,
    lookup: state.language.lookup,
  }));
  const [showError, setShowError] = useState(false);

  const handleCancel = () => {
    history.push("/subscriber");
  };

  const handleClose = () => {
    setShowError(false);
  };

  return (
    <React.Fragment>
      <Formik
        validateOnChange={true}
        initialValues={{
          phone_number: "",
          language: "",
        }}
        validationSchema={validationSchema}
        onSubmit={(data, { setSubmitting, setErrors }) => {
          setSubmitting(true);

          dispatch(
            addSubscriber(data, history, (err) => {
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
              <CardHeader subheader="Add a subscriber" title="Subscriber" />
              <Divider />
              <CardContent>
                <Grid container spacing={3}>
                  <Grid item md={12} xs={12}>
                    <Field
                      mask={phoneMask}
                      placeholder="Phone Number"
                      name="phone_number"
                      label="Phone Number"
                      type="input"
                      variant="outlined"
                      as={MaskedInputField}
                    />
                  </Grid>
                  <Grid item md={12} xs={12}>
                    <Field
                      name="language"
                      variant="outlined"
                      label="Language"
                      as={SelectField}
                    >
                      {lookup.map((l) => (
                        <MenuItem key={l.value} value={l.value}>
                          {l.label}
                        </MenuItem>
                      ))}
                    </Field>
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

SubscriberAdd.propTypes = {
  className: PropTypes.string,
};

export default SubscriberAdd;
