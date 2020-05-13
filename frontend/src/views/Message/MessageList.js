import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/styles";
import { useDispatch, useSelector } from "react-redux";
import Alert from "@material-ui/lab/Alert";
import CircularProgress from "@material-ui/core/CircularProgress";
import Box from "@material-ui/core/Box";
import Snackbar from "@material-ui/core/Snackbar";
import { MessagesToolbar, MessagesTable } from "./components";
import { fetchMessages, resetSaveMessageSuccess } from "../../store/actions";
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

const MessageList = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const [limit, setLimit] = useState(Constants.PAGE_SIZE); //limit
  const [offset, setOffset] = useState(0); // page
  const [searchTerm, setSearchTerm] = useState("");

  //redux
  const {
    error,
    loadingMessages,
    messages,
    count,
    saveSuccess,
    loadingLanguageLookup,
    loadingChannelLookup,
  } = useSelector((state) => ({
    error: state.message.error,
    loadingMessages: state.message.loadingMessages,
    messages: state.message.data,
    count: state.message.count,
    saveSuccess: state.message.saveSuccess,
    loadingLanguageLookup: state.language.loadingLookup,
    loadingChannelLookup: state.channel.loadingLookup,
  }));

  const handleClose = (event, reason) => {
    dispatch(resetSaveMessageSuccess());
  };

  const handleSearchTermChange = (searchTerm) => {
    setSearchTerm(searchTerm);
  };

  useEffect(() => {
    dispatch(fetchMessages(limit, offset * limit, searchTerm)); //rowPerPage, page
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
  } else if (loadingMessages || loadingLanguageLookup || loadingChannelLookup) {
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
        <MessagesTable
          messages={messages}
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
      <MessagesToolbar
        onSearchTermChange={handleSearchTermChange}
        disableButtons={
          loadingMessages || loadingLanguageLookup || loadingChannelLookup
        }
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

export default MessageList;
