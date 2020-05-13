import React, { useEffect, useRef, useState } from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import PerfectScrollbar from "react-perfect-scrollbar";
import { makeStyles } from "@material-ui/styles";
import {
  Card,
  CardActions,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TablePagination,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@material-ui/core";

import MessageRow from "./MessageRow";

const useStyles = makeStyles((theme) => ({
  root: {},
  content: {
    padding: 0,
  },
  inner: {
    minWidth: 650,
  },
  actions: {
    justifyContent: "flex-end",
  },

  container: {
    dispaly: "flex",
    flexDirection: "column",
  },
}));

const MessagesTable = (props) => {
  //const { className, messages, count, ...rest } = props;

  const classes = useStyles();
  const [open, setOpen] = useState(false);
  const [messageStatus, setMessageStatus] = useState();

  const handleDialogOpen = (messageStatus) => {
    if (messageStatus !== undefined) {
      setMessageStatus(messageStatus);
      setOpen(true);
    }
  };

  const handleClose = () => {
    setOpen(false);
  };

  const descriptionElementRef = useRef(null);
  useEffect(() => {
    if (open) {
      const { current: descriptionElement } = descriptionElementRef;
      if (descriptionElement !== null) {
        descriptionElement.focus();
      }
    }
  }, [open]);

  const handlePageChange = (event, page) => {
    props.setoffset(page);
  };

  const handleRowsPerPageChange = (event) => {
    props.setlimit(event.target.value);
  };

  return (
    <React.Fragment>
      <Card {...props.rest} className={clsx(classes.root, props.className)}>
        <CardContent className={classes.content}>
          <PerfectScrollbar>
            <div className={classes.inner}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell style={{ minWidth: 100 }}>Message</TableCell>
                    <TableCell>Channels</TableCell>
                    <TableCell>Languages</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {props.messages.map((msg) => (
                    <MessageRow
                      message={msg}
                      key={msg.id}
                      openDialog={(id) => handleDialogOpen(id)}
                    />
                  ))}
                </TableBody>
              </Table>
            </div>
          </PerfectScrollbar>
        </CardContent>
        <CardActions className={classes.actions}>
          <TablePagination
            component="div"
            count={props.count}
            onChangePage={handlePageChange}
            onChangeRowsPerPage={handleRowsPerPageChange}
            page={props.offset}
            rowsPerPage={props.limit}
            rowsPerPageOptions={[5, 10, 25]}
          />
        </CardActions>
      </Card>
      <Dialog
        open={open}
        onClose={handleClose}
        scroll={"paper"}
        aria-labelledby="msg-dialog-title"
        aria-describedby="msg-detail-dialog"
        fullWidth={true}
        maxWidth="sm"
      >
        <DialogTitle id="msg-dialog-title">Message Status</DialogTitle>
        <DialogContent dividers={true}>
          <DialogContentText
            id="msg-detail-dialog"
            ref={descriptionElementRef}
            tabIndex={-1}
          >
            <span className={classes.container}>
              {messageStatus &&
                messageStatus.map((status, index) => (
                  <span key={index} className={classes.container}>
                    <br />
                    <strong>{status.name}</strong>
                    <br />
                    &nbsp; Sent: {status.success_count}
                    <br />
                    &nbsp; Failed: {status.error_count}
                    <br />
                    &nbsp; Config Error:{" "}
                    {status.config_error ? "True" : "False"}
                  </span>
                ))}
            </span>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

MessagesTable.propTypes = {
  className: PropTypes.string,
  messages: PropTypes.array.isRequired,
  count: PropTypes.number.isRequired,
  limit: PropTypes.number.isRequired,
  offset: PropTypes.number.isRequired,
  setlimit: PropTypes.func.isRequired,
  setoffset: PropTypes.func.isRequired,
};

export default MessagesTable;
