import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/styles";
import { useDispatch, useSelector } from "react-redux";
import Alert from "@material-ui/lab/Alert";
import CircularProgress from "@material-ui/core/CircularProgress";
import Box from "@material-ui/core/Box";
import Snackbar from "@material-ui/core/Snackbar";
import { SurveyToolbar, SurveyTable } from "./components";
import { fetchSurveys, resetSaveSurveySuccess } from "../../store/actions";
import * as Constants from "../../helpers/constants";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(3),
  },
  content: {
    marginTop: theme.spacing(2),
  },
  message: {
    marginLeft: theme.spacing(0),
  },
}));

const SurveyList = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const [limit, setLimit] = useState(Constants.PAGE_SIZE); //limit
  const [offset, setOffset] = useState(0); // page
  const [searchTerm, setSearchTerm] = useState("");

  //redux
  const { error, loadingSurveys, surveys, count, saveSuccess } = useSelector(
    (state) => ({
      error: state.survey.error,
      loadingSurveys: state.survey.loadingSurveys,
      surveys: state.survey.data,
      count: state.survey.count,
      saveSuccess: state.survey.saveSuccess,
    })
  );

  const handleClose = (event, reason) => {
    dispatch(resetSaveSurveySuccess());
  };

  const handleSearchTermChange = (searchTerm) => {
    setSearchTerm(searchTerm);
  };

  useEffect(() => {
    dispatch(fetchSurveys(limit, offset * limit, searchTerm)); //rowPerPage, page
  }, [dispatch, limit, offset, searchTerm]);

  let content = null;
  if (error) {
    content = (
      <Box
        display="flex"
        justifyContent="center"
        m={1}
        p={1}
        bgcolor="background.paper"
        className={classes.message}
      >
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  } else if (loadingSurveys) {
    content = (
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
    );
  } else {
    content = (
      <div className={classes.content}>
        <SurveyTable
          surveys={surveys}
          count={count}
          limit={limit}
          offset={offset}
          setlimit={setLimit}
          setoffset={setOffset}
        />
      </div>
    );
  }
  return (
    <div className={classes.root}>
      <SurveyToolbar
        onSearchTermChange={handleSearchTermChange}
        disableButtons={loadingSurveys}
      />
      {content}
      <Snackbar
        open={saveSuccess}
        autoHideDuration={5000}
        onClose={handleClose}
      >
        <Alert onClose={handleClose} severity="success">
          Success
        </Alert>
      </Snackbar>
    </div>
  );
};

export default SurveyList;
