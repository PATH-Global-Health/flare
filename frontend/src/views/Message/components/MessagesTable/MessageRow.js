import React from "react";
import {
  TableCell,
  TableRow,
  Typography,
  Chip,
  Avatar,
} from "@material-ui/core";
import InfoIcon from "@material-ui/icons/Info";
import MessageIcon from "@material-ui/icons/Message";
import { makeStyles } from "@material-ui/styles";
import { useSelector } from "react-redux";
import PropTypes from "prop-types";

const useStyles = makeStyles((theme) => ({
  root: {},
  menu: {
    minWidth: 40,
  },

  blue: {
    borderColor: "#3f51b5",
    color: "#3f51b5",
  },

  orange: {
    borderColor: "#FF8A3C",
    color: "#FF8A3C",
  },

  red: {
    borderColor: "#e53935",
    color: "#e53935",
  },

  nameContainer: {
    display: "flex",
    alignItems: "flex-start",
  },

  avatar: {
    marginRight: theme.spacing(2),
  },

  white: {
    borderColor: "#fff",
    color: "#fff",
  },
}));

const MessageRow = (props) => {
  const { message } = props;
  const classes = useStyles();

  const { channelLookup, languageLookup } = useSelector((state) => ({
    channelLookup: state.channel.lookup,
    languageLookup: state.language.lookup,
  }));

  let c = classes.blue;
  if (message.status === "started") {
    c = classes.orange;
  } else if (message.status === "error") {
    c = classes.red;
  }

  const { channels } = props.message;
  const chnls = [];

  if (channels) {
    channels.forEach((channel) => {
      channelLookup.forEach((c) => {
        if (channel === c.value) {
          chnls.push(<div key={c.value}>{c.label}</div>);
        }
      });
    });
  }

  const { languages } = props.message;
  const langs = [];

  if (languages) {
    languages.forEach((lang) => {
      languageLookup.forEach((l) => {
        if (lang === l.value) {
          langs.push(<div key={l.value}>{l.label}</div>);
        }
      });
    });
  }

  return (
    <TableRow className={classes.tableRow} hover key={message.id} size="small">
      <TableCell>
        <div className={classes.nameContainer}>
          <Avatar className={classes.avatar}>
            <MessageIcon />
          </Avatar>
          <Typography variant="body1">{message.content}</Typography>
        </div>
      </TableCell>
      <TableCell>{chnls}</TableCell>
      <TableCell>{langs}</TableCell>
      <TableCell>
        {message.status && (
          <Chip
            icon={<InfoIcon className={c} />}
            label="Primary clickable"
            clickable
            label={message.status}
            variant="outlined"
            className={c}
            onClick={() => props.openDialog(message.status_detail)}
          />
        )}
      </TableCell>
    </TableRow>
  );
};

MessageRow.propTypes = {
  message: PropTypes.object.isRequired,
  openDialog: PropTypes.func.isRequired,
};

export default MessageRow;
