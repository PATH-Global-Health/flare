import React, { useState } from "react";
import { TableCell, TableRow, Typography, IconButton } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
// import { useHistory } from "react-router-dom";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import PropTypes from "prop-types";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import DeleteIcon from "@material-ui/icons/Delete";

const useStyles = makeStyles((theme) => ({
  root: {},
  menu: {
    minWidth: 40,
  },
}));

const ResultRow = (props) => {
  const { result } = props;
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  // let history = useHistory();

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleDelete = (id) => {
    setAnchorEl(null);
    props.openDialog(id);
  };

  return (
    <TableRow className={classes.tableRow} hover key={result.id} size="small">
      <TableCell>
        <Typography variant="body1">{result.phone_number}</Typography>
      </TableCell>
      <TableCell>{result.session_id}</TableCell>
      <TableCell>{result.completed ? "Yes" : "No"}</TableCell>
      <TableCell>{result.posted ? "Yes" : "No"}</TableCell>
      <TableCell>{result.rejected ? "Yes" : "No"}</TableCell>
      <TableCell>
        <IconButton
          aria-label="more"
          aria-controls="action-menu"
          aria-haspopup="true"
          onClick={handleClick}
        >
          <MoreVertIcon />
        </IconButton>
        <Menu
          id="action-menu"
          anchorEl={anchorEl}
          keepMounted
          open={Boolean(anchorEl)}
          onClose={handleClose}
        >
          <MenuItem onClick={() => handleDelete(result.id)}>
            <ListItemIcon className={classes.menu}>
              <DeleteIcon fontSize="small" />
            </ListItemIcon>
            Delete
          </MenuItem>
        </Menu>
      </TableCell>
    </TableRow>
  );
};

ResultRow.propTypes = {
  result: PropTypes.object.isRequired,
  openDialog: PropTypes.func.isRequired,
};

export default ResultRow;
