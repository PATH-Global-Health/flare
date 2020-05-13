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
import StorageIcon from "@material-ui/icons/Storage";

const useStyles = makeStyles((theme) => ({
  root: {},
  menu: {
    minWidth: 40,
  },
}));

const SurveyRow = (props) => {
  const { survey } = props;
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

  const handleEdit = (id) => {
    history.push(`/survey/edit/${id}`);
  };

  const handleListData = (id) => {
    history.push(`/result/${id}`);
  };

  return (
    <TableRow className={classes.tableRow} hover key={survey.id} size="small">
      <TableCell>
        <Typography variant="body1">{survey.title}</Typography>
      </TableCell>
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
          <MenuItem onClick={() => handleListData(survey.id)}>
            <ListItemIcon className={classes.menu}>
              <StorageIcon fontSize="small" />
            </ListItemIcon>
            Data
          </MenuItem>
          <MenuItem onClick={() => handleEdit(survey.id)}>
            <ListItemIcon className={classes.menu}>
              <EditIcon fontSize="small" />
            </ListItemIcon>
            Edit
          </MenuItem>

          <MenuItem onClick={() => handleDelete(survey.id)}>
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

SurveyRow.propTypes = {
  survey: PropTypes.object.isRequired,
  openDialog: PropTypes.func.isRequired,
};

export default SurveyRow;
