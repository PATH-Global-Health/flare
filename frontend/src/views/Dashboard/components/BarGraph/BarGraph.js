import React from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import { Bar } from "react-chartjs-2";
import { makeStyles } from "@material-ui/styles";
import { Card, CardHeader, CardContent, Divider } from "@material-ui/core";
import palette from "../../../../theme/palette";

import { options } from "../../../../helpers/chart";

const useStyles = makeStyles(() => ({
  root: {},
  chartContainer: {
    height: 400,
    position: "relative",
  },
  actions: {
    justifyContent: "flex-end",
  },
}));

const BarGraph = (props) => {
  const { className, ...rest } = props;

  const classes = useStyles();

  let content = null;
  if (props.data) {
    let d = props.data.datasets[0];
    d = {
      ...d,
      backgroundColor: palette.primary.main,
      barThickness: 12,
      maxBarThickness: 10,
      barPercentage: 0.5,
      categoryPercentage: 0.5,
    };
    props.data.datasets[0] = d;
    content = <Bar data={props.data} options={options} />;
  }

  return (
    <Card {...rest} className={clsx(classes.root, className)}>
      <CardHeader title={props.title} />
      <Divider />
      <CardContent>
        <div className={classes.chartContainer}>{props.data && content}</div>
      </CardContent>
    </Card>
  );
};

BarGraph.propTypes = {
  className: PropTypes.string,
  data: PropTypes.object,
  title: PropTypes.string,
};

export default BarGraph;
