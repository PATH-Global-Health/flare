import React from "react";
import { Doughnut } from "react-chartjs-2";
import clsx from "clsx";
import PropTypes from "prop-types";
import { makeStyles, useTheme } from "@material-ui/styles";
import {
  Card,
  CardHeader,
  CardContent,
  Divider,
  Typography,
} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  root: {
    height: "100%",
  },
  chartContainer: {
    position: "relative",
    height: "300px",
  },
  stats: {
    marginTop: theme.spacing(2),
    display: "flex",
    justifyContent: "center",
  },
  device: {
    textAlign: "center",
    padding: theme.spacing(1),
  },
  deviceIcon: {
    color: theme.palette.icon,
  },
}));

const Pie = (props) => {
  const { className, ...rest } = props;

  const classes = useStyles();
  const theme = useTheme();

  const options = {
    legend: {
      display: false,
    },
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    cutoutPercentage: 80,
    layout: { padding: 0 },
    tooltips: {
      enabled: true,
      mode: "index",
      intersect: false,
      borderWidth: 1,
      borderColor: theme.palette.divider,
      backgroundColor: theme.palette.white,
      titleFontColor: theme.palette.text.primary,
      bodyFontColor: theme.palette.text.secondary,
      footerFontColor: theme.palette.text.secondary,
    },
  };

  const devices = [
    {
      title: "Male",
      value: "63",
      color: theme.palette.primary.main,
    },
    {
      title: "Female",
      value: "15",
      color: theme.palette.error.main,
    },
  ];

  let content = null;

  if (props.data) {
    let d = props.data.datasets[0];
    d = {
      ...d,
      backgroundColor: [theme.palette.primary.main, theme.palette.error.main],
      borderWidth: 8,
      borderColor: theme.palette.white,
      hoverBorderColor: theme.palette.white,
    };
    props.data.datasets[0] = d;

    devices[0].value = d.data[0];
    devices[1].value = d.data[1];

    content = (
      <React.Fragment>
        <div className={classes.chartContainer}>
          <Doughnut data={props.data} options={options} />
        </div>
        <div className={classes.stats}>
          {devices.map((device) => (
            <div className={classes.device} key={device.title}>
              <span className={classes.deviceIcon}>{device.icon}</span>
              <Typography variant="body1">{device.title}</Typography>
              <Typography style={{ color: device.color }} variant="h2">
                {device.value}%
              </Typography>
            </div>
          ))}
        </div>
      </React.Fragment>
    );
  }

  return (
    <Card {...rest} className={clsx(classes.root, className)}>
      <CardHeader title={props.title} />
      <Divider />
      <CardContent>{props.data && content}</CardContent>
    </Card>
  );
};

Pie.propTypes = {
  className: PropTypes.string,
  data: PropTypes.object,
};

export default Pie;
