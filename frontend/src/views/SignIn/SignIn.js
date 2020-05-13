import React, { useState, useEffect } from "react";
import validate from "validate.js";
import { makeStyles } from "@material-ui/styles";
import { Grid, Button, TextField, Typography, Link } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import CircularProgress from "@material-ui/core/CircularProgress";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../../store/actions";
import style from "./style";

const schema = {
  username: {
    presence: { allowEmpty: false, message: "is required" },
    length: {
      maximum: 64,
    },
  },
  password: {
    presence: { allowEmpty: false, message: "is required" },
    length: {
      maximum: 128,
    },
  },
};

const useStyles = makeStyles(style);

const SignIn = (props) => {
  const classes = useStyles();

  const [formState, setFormState] = useState({
    isValid: false,
    values: {},
    touched: {},
    errors: {},
  });

  useEffect(() => {
    const errors = validate(formState.values, schema);

    setFormState((formState) => ({
      ...formState,
      isValid: errors ? false : true,
      errors: errors || {},
    }));
  }, [formState.values]);

  const handleChange = (event) => {
    event.persist();

    setFormState((formState) => ({
      ...formState,
      values: {
        ...formState.values,
        [event.target.name]:
          event.target.type === "checkbox"
            ? event.target.checked
            : event.target.value,
      },
      touched: {
        ...formState.touched,
        [event.target.name]: true,
      },
    }));
  };

  const hasError = (field) =>
    formState.touched[field] && formState.errors[field] ? true : false;

  //redux
  const { error, loading, isAuthenticated } = useSelector((state) => ({
    error: state.security.error,
    loading: state.security.loading,
    isAuthenticated: state.security.isAuthenticated,
  }));

  useEffect(() => {
    if (isAuthenticated) {
      props.history.push("/dashboard");
    }
  }, [isAuthenticated, props.history]);

  const dispatch = useDispatch();

  function handleSubmit(e) {
    e.preventDefault();
    const { username, password } = formState.values;

    dispatch(login(username, password));
  }

  return (
    <div className={classes.root}>
      <Grid className={classes.grid} container>
        <Grid className={classes.quoteContainer} item lg={5}>
          <div className={classes.quote}>
            <div className={classes.quoteInner}>
              <Typography className={classes.quoteText} variant="h1">
                USSD based messaging system
              </Typography>
              <div className={classes.person}>
                <Typography variant="body1">
                  &copy;{" "}
                  <Link component="a" href="https://path.org" target="_blank">
                    PATH
                  </Link>
                  . 2020
                </Typography>
              </div>
            </div>
          </div>
        </Grid>
        <Grid className={classes.content} item lg={7} xs={12}>
          <div className={classes.content}>
            <div className={classes.contentHeader}>&nbsp;</div>
            <div className={classes.contentBody}>
              <form className={classes.form} onSubmit={handleSubmit}>
                <Typography className={classes.title} variant="h2">
                  Sign in
                </Typography>
                {error && <Alert severity="error">{error}</Alert>}
                <TextField
                  className={classes.textField}
                  error={hasError("username")}
                  fullWidth
                  helperText={
                    hasError("username") ? formState.errors.username[0] : null
                  }
                  label="Username"
                  name="username"
                  onChange={handleChange}
                  type="text"
                  value={formState.values.username || ""}
                  variant="outlined"
                />
                <TextField
                  className={classes.textField}
                  error={hasError("password")}
                  fullWidth
                  helperText={
                    hasError("password") ? formState.errors.password[0] : null
                  }
                  label="Password"
                  name="password"
                  onChange={handleChange}
                  type="password"
                  value={formState.values.password || ""}
                  variant="outlined"
                />
                {loading ? (
                  <CircularProgress className={classes.spinner} />
                ) : (
                  <Button
                    className={classes.signInButton}
                    color="primary"
                    disabled={!formState.isValid}
                    fullWidth
                    size="large"
                    type="submit"
                    variant="contained"
                  >
                    Sign in now
                  </Button>
                )}
              </form>
            </div>
          </div>
        </Grid>
      </Grid>
    </div>
  );
};

export default SignIn;
