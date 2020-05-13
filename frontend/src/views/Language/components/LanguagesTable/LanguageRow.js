import React, { useState } from "react";
import { TableCell, TableRow, Typography, IconButton } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import { useHistory } from "react-router-dom";
import MoreVertIcon from "@material-ui/icons/MoreVert";
import Menu from "@material-ui/core/Menu";
import MenuItem from "@material-ui/core/MenuItem";
import PropTypes from "prop-types";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import EditIcon from "@material-ui/icons/Edit";
import DeleteIcon from "@material-ui/icons/Delete";

const useStyles = makeStyles((theme) => ({
  root: {},
  menu: {
    minWidth: 40,
  },
}));

const LanguageRow = (props) => {
  const { language } = props;
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  let history = useHistory();

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

  const handleEdit = () => {
    history.push(`/language/edit/${language.id}`);
  };

  return (
    <TableRow className={classes.tableRow} hover key={language.id} size="small">
      <TableCell>
        <Typography variant="body1">{language.name}</Typography>
      </TableCell>
      <TableCell>{language.code}</TableCell>
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
          <MenuItem onClick={handleEdit}>
            <ListItemIcon className={classes.menu}>
              <EditIcon fontSize="small" />
            </ListItemIcon>
            Edit
          </MenuItem>

          <MenuItem onClick={() => handleDelete(language.id)}>
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

LanguageRow.propTypes = {
  language: PropTypes.object.isRequired,
  openDialog: PropTypes.func.isRequired,
};

export default LanguageRow;
