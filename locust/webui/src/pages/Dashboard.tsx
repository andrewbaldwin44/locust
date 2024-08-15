import CssBaseline from '@mui/material/CssBaseline';
import { Theme, ThemeProvider } from '@mui/material/styles';
import { connect } from 'react-redux';

import Layout from 'components/Layout/Layout';
import useLogViewer from 'components/LogViewer/useLogViewer';
import SwarmForm from 'components/SwarmForm/SwarmForm';
import Tabs from 'components/Tabs/Tabs';
import { SWARM_STATE } from 'constants/swarm';
import useCreateTheme from 'hooks/useCreateTheme';
import useSwarmUi from 'hooks/useSwarmUi';
import { IRootState } from 'redux/store';
import { ITab } from 'types/tab.types';
import { SwarmState } from 'types/ui.types';

interface IDashboard {
  isModalOpen?: boolean;
  swarmState: SwarmState;
  extendedTabs?: ITab[];
  extendedTheme?: Theme;
  tabs?: ITab[];
}

function Dashboard({ swarmState, tabs, extendedTabs, extendedTheme }: IDashboard) {
  useSwarmUi();
  useLogViewer();

  const theme = useCreateTheme(extendedTheme);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Layout>
        {swarmState === SWARM_STATE.READY ? (
          <SwarmForm />
        ) : (
          <Tabs extendedTabs={extendedTabs} tabs={tabs} />
        )}
      </Layout>
    </ThemeProvider>
  );
}

const storeConnector = ({ swarm: { state } }: IRootState) => ({
  swarmState: state,
});

export default connect(storeConnector)(Dashboard);
