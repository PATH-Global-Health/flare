import React, { useState } from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import PerfectScrollbar from "react-perfect-scrollbar";
import { useHistory } from "react-router-dom";
import { useDispatch } from "react-redux";
import { makeStyles } from "@material-ui/styles";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TablePagination,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@material-ui/core";

import ResultRow from "./ResultRow";
import { deleteResult } from "../../../../store/actions";

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
}));

const ResultsTable = (props) => {
  //const { className, results, count, ...rest } = props;

  const classes = useStyles();
  let history = useHistory();
  const dispatch = useDispatch();

  const [open, setDialogOpen] = useState(false);
  const [selectedId, setSelectedId] = useState();

  const handleDialogOpen = (id) => {
    setSelectedId(id);
    setDialogOpen(true);
  };

  const handleYesDialogButton = () => {
    setDialogOpen(false);
    dispatch(deleteResult(selectedId, history));
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
  };

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
                    <TableCell>Phone Number</TableCell>
                    <TableCell>Session Id</TableCell>
                    <TableCell>Completed</TableCell>
                    <TableCell>Posted</TableCell>
                    <TableCell>Rejected</TableCell>
                    <TableCell>Action</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {props.results.map((result) => (
                    <ResultRow
                      result={result}
                      key={result.id}
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
        onClose={handleDialogClose}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Delete result?"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to remove this response
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDialogClose} color="primary">
            No
          </Button>
          <Button onClick={handleYesDialogButton} color="primary" autoFocus>
            Yes
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
};

ResultsTable.propTypes = {
  className: PropTypes.string,
  results: PropTypes.array.isRequired,
  count: PropTypes.number.isRequired,
  limit: PropTypes.number.isRequired,
  offset: PropTypes.number.isRequired,
  setlimit: PropTypes.func.isRequired,
  setoffset: PropTypes.func.isRequired,
};

export default ResultsTable;
