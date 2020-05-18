import React, { useEffect } from "react";
import { Link as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/styles";
import { Avatar, Typography } from "@material-ui/core";
import { useDispatch, useSelector } from "react-redux";
import CircularProgress from "@material-ui/core/CircularProgress";
import { fetchUser } from "../../../../../../store/actions";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    minHeight: "fit-content",
  },
  avatar: {
    width: 60,
    height: 60,
  },
  name: {
    marginTop: theme.spacing(1),
  },
}));

const Profile = (props) => {
  const { className, ...rest } = props;

  const classes = useStyles();
  const dispatch = useDispatch();

  //redux
  const { error, loading, data } = useSelector((state) => ({
    error: state.user.error,
    loading: state.user.loading,
    data: state.user.data,
  }));

  let content = null;

  if (error) {
    content = <div>{error}</div>;
  } else if (loading) {
    content = <CircularProgress size={30} thickness={1.5} />;
  } else {
    const user = {
      name: data.username,
      avatar: "/images/avatars/avatar.png",
      bio: data.email,
    };

    content = (
      <React.Fragment>
        <Avatar
          alt="Person"
          className={classes.avatar}
          component={RouterLink}
          src={user.avatar}
          to="/settings"
        />
        <Typography className={classes.name} variant="h4">
          {user.name}
        </Typography>
        <Typography variant="body2">{user.bio}</Typography>
      </React.Fragment>
    );
  }
  useEffect(() => {
    dispatch(fetchUser());
  }, [dispatch]);

  return (
    <div {...rest} className={clsx(classes.root, className)}>
      {content}
    </div>
  );
};

Profile.propTypes = {
  className: PropTypes.string,
};

export default Profile;
