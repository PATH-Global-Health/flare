import React, { useState } from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import { makeStyles } from "@material-ui/styles";
import { Button } from "@material-ui/core";
import { useHistory } from "react-router-dom";

import { SearchInput } from "../../../../components";

const useStyles = makeStyles((theme) => ({
  root: {},
  row: {
    height: "42px",
    display: "flex",
    alignItems: "center",
    marginTop: theme.spacing(1),
  },
  spacer: {
    flexGrow: 1,
  },
  importButton: {
    marginRight: theme.spacing(1),
  },
  exportButton: {
    marginRight: theme.spacing(1),
  },
  searchInput: {
    marginRight: theme.spacing(1),
  },
}));

const SubscribersToolbar = (props) => {
  const { className, onSearchTermChange, disableButtons, ...rest } = props;

  const classes = useStyles();
  let history = useHistory();
  const [searchTerm, setSearchTerm] = useState("");

  const handleClick = () => {
    history.push("/subscriber/add");
  };

  const onKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (onSearchTermChange !== undefined) {
        onSearchTermChange(searchTerm);
      }
    }
  };

  const onChange = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div {...rest} className={clsx(classes.root, className)}>
      <div className={classes.row}>
        <span className={classes.spacer} />
        <Button className={classes.exportButton} disabled={disableButtons}>
          Export
        </Button>
        <Button
          color="primary"
          variant="contained"
          onClick={handleClick}
          disabled={disableButtons}
        >
          Add subscriber
        </Button>
      </div>
      <div className={classes.row}>
        <SearchInput
          className={classes.searchInput}
          placeholder="Search subscriber"
          onChange={onChange}
          onKeyPress={onKeyPress}
          disabled={disableButtons}
        />
      </div>
    </div>
  );
};

SubscribersToolbar.propTypes = {
  className: PropTypes.string,
  onSearchTermChange: PropTypes.func,
  disableButtons: PropTypes.bool,
};

export default SubscribersToolbar;
