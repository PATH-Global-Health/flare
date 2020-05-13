import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/styles";
import { useDispatch, useSelector } from "react-redux";
import Alert from "@material-ui/lab/Alert";
import CircularProgress from "@material-ui/core/CircularProgress";
import Box from "@material-ui/core/Box";
import Snackbar from "@material-ui/core/Snackbar";
import { SubscribersToolbar, SubscribersTable } from "./components";
import {
  fetchSubscribers,
  resetSaveSubscriberSuccess,
} from "../../store/actions";
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

const SubscriberList = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const [limit, setLimit] = useState(Constants.PAGE_SIZE); //limit
  const [offset, setOffset] = useState(0); // page
  const [searchTerm, setSearchTerm] = useState("");

  //redux
  const {
    error,
    loadingSubscribers,
    subscribers,
    count,
    saveSuccess,
    loadingLookup,
  } = useSelector((state) => ({
    error: state.subscriber.error,
    loadingSubscribers: state.subscriber.loadingSubscribers,
    subscribers: state.subscriber.data,
    count: state.subscriber.count,
    saveSuccess: state.subscriber.saveSuccess,
    loadingLookup: state.language.loadingLookup,
  }));

  const handleClose = (event, reason) => {
    dispatch(resetSaveSubscriberSuccess());
  };

  const handleSearchTermChange = (searchTerm) => {
    setSearchTerm(searchTerm);
  };

  useEffect(() => {
    dispatch(fetchSubscribers(limit, offset * limit, searchTerm)); //rowPerPage, page
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
  } else if (loadingSubscribers || loadingLookup) {
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
        <SubscribersTable
          subscribers={subscribers}
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
      <SubscribersToolbar
        onSearchTermChange={handleSearchTermChange}
        disableButtons={loadingSubscribers || loadingLookup}
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

export default SubscriberList;
