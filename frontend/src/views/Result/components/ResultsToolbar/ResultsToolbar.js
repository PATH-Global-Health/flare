import React, { useState } from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import { makeStyles } from "@material-ui/styles";
import { IconButton } from "@material-ui/core";
import { useHistory } from "react-router-dom";
import ArrowBackIcon from "@material-ui/icons/ArrowBack";
import { SearchInput } from "../../../../components";

const useStyles = makeStyles((theme) => ({
  root: {},
  row: {
    height: "42px",
    display: "flex",
    alignItems: "center",
    marginTop: theme.spacing(1),
  },
  back: {
    alignItems: "left",
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

const ResultsToolbar = (props) => {
  const { className, onSearchTermChange, disableButtons, ...rest } = props;

  const classes = useStyles();
  let history = useHistory();
  const [searchTerm, setSearchTerm] = useState("");

  const handleBack = () => {
    history.push("/survey/");
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
        <div className={classes.left}>
          <IconButton onClick={handleBack}>
            <ArrowBackIcon />
          </IconButton>
        </div>
        <span className={classes.spacer} />
      </div>
      <div className={classes.row}>
        <SearchInput
          className={classes.searchInput}
          placeholder="Search result"
          onChange={onChange}
          onKeyPress={onKeyPress}
          disabled={disableButtons}
        />
      </div>
    </div>
  );
};

ResultsToolbar.propTypes = {
  className: PropTypes.string,
  onSearchTermChange: PropTypes.func,
  disableButtons: PropTypes.bool,
};

export default ResultsToolbar;
