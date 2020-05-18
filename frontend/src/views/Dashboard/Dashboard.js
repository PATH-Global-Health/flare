import React, { useEffect } from "react";
import { makeStyles } from "@material-ui/styles";
import { Grid } from "@material-ui/core";
import { useDispatch, useSelector } from "react-redux";
import Alert from "@material-ui/lab/Alert";
import CircularProgress from "@material-ui/core/CircularProgress";
import Box from "@material-ui/core/Box";
import { fetchDashboardData } from "../../store/actions";

import {
  Messages,
  Subscribers,
  Surveys,
  Suspects,
  Pie,
  BarGraph,
} from "./components";

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(4),
  },
  dashboard: {
    marginLeft: theme.spacing(0),
  },
}));

const Dashboard = () => {
  const classes = useStyles();
  const dispatch = useDispatch();

  //redux
  const { error, loading, data } = useSelector((state) => ({
    error: state.dashboard.error,
    loading: state.dashboard.loading,
    data: state.dashboard.data,
  }));

  useEffect(() => {
    dispatch(fetchDashboardData());
  }, [dispatch]);

  let content = null;
  if (error) {
    content = (
      <Box
        display="flex"
        justifyContent="center"
        m={1}
        p={1}
        bgcolor="background.paper"
        className={classes.dashboard}
      >
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  } else if (loading) {
    content = (
      <Box
        display="flex"
        justifyContent="center"
        m={1}
        p={1}
        bgcolor="background.paper"
        className={classes.dashboard}
      >
        <CircularProgress size={100} thickness={1.5} />
      </Box>
    );
  } else {
    content = (
      <Grid container spacing={4}>
        <Grid item lg={3} sm={6} xl={3} xs={12}>
          <Messages data={data.total_messages ? data.total_messages : "-"} />
        </Grid>
        <Grid item lg={3} sm={6} xl={3} xs={12}>
          <Subscribers
            data={data.total_subscribers ? data.total_subscribers : "-"}
          />
        </Grid>
        <Grid item lg={3} sm={6} xl={3} xs={12}>
          <Surveys data={data.total_surveys ? data.total_surveys : "-"} />
        </Grid>
        <Grid item lg={3} sm={6} xl={3} xs={12}>
          <Suspects data={data.total_suspects ? data.total_suspects : "-"} />
        </Grid>
        <Grid item lg={8} md={12} xl={9} xs={12}>
          <BarGraph title="Suspects by age" data={data.suspects_by_age} />
        </Grid>
        <Grid item lg={4} md={6} xl={3} xs={12}>
          <Pie title="Suspects by sex" data={data.suspects_by_sex} />
        </Grid>
        <Grid item lg={12} md={12} xl={3} xs={12}>
          <BarGraph title="Suspects by region" data={data.suspects_by_region} />
        </Grid>
      </Grid>
    );
  }
  return <div className={classes.root}>{content}</div>;
};

export default Dashboard;
