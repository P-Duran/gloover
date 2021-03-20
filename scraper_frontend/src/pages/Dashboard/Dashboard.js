import React from 'react';
import JobTable from './Jobs/JobTable'
import { Box, Grid } from '@material-ui/core';
import { withRouter } from 'react-router';
import { JobStates } from 'utils/jobUtils';
import { ActiveJobStates } from 'utils/jobUtils';

export const Dashboard = withRouter(({ history }) => {

  return (
    <Grid container justify='flex-end' style={{ padding: 24 }}>
      <JobTable main={true} tableTitle={'Running Jobs'} filterJobs={job => ActiveJobStates.includes(job.state)}></JobTable>
      <Box margin={2}></Box>
      <JobTable tableTitle={'Finished Jobs'} filterJobs={job => job.state === JobStates.FINISHED}></JobTable>
      <Box margin={2}></Box>
      <JobTable tableTitle={'Cancelled Jobs'} filterJobs={job => job.state === JobStates.CANCELLED}></JobTable>
    </Grid>
  );
});
