import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/styles";
import { useDispatch, useSelector } from "react-redux";
import Alert from "@material-ui/lab/Alert";
import CircularProgress from "@material-ui/core/CircularProgress";
import Box from "@material-ui/core/Box";
import Snackbar from "@material-ui/core/Snackbar";
import { ResultsToolbar, ResultsTable } from "./components";
import { fetchResults, resetDeleteResultSuccess } from "../../store/actions";
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

const ResultList = (props) => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const [limit, setLimit] = useState(Constants.PAGE_SIZE); //limit
  const [offset, setOffset] = useState(0); // page
  const [searchTerm, setSearchTerm] = useState("");

  //redux
  const { error, loadingResults, results, count, deleteSuccess } = useSelector(
    (state) => ({
      error: state.result.error,
      loadingResults: state.result.loadingResults,
      results: state.result.data,
      count: state.result.count,
      deleteSuccess: state.result.deleteSuccess,
    })
  );

  const handleClose = (event, reason) => {
    dispatch(resetDeleteResultSuccess());
  };

  const handleSearchTermChange = (searchTerm) => {
    setSearchTerm(searchTerm);
  };

  useEffect(() => {
    dispatch(
      fetchResults(props.match.params.id, limit, offset * limit, searchTerm)
    ); //rowPerPage, page
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
  } else if (loadingResults) {
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
        <ResultsTable
          results={results}
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
      <ResultsToolbar
        onSearchTermChange={handleSearchTermChange}
        disableButtons={loadingResults}
      />
      {content}
      <Snackbar
        open={deleteSuccess}
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

export default ResultList;
