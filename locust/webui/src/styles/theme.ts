import { PaletteMode, createTheme as baseCreateTheme } from '@mui/material';
import { Theme } from '@mui/material/styles';
import { deepmerge } from '@mui/utils';

const defaultExtendedTheme = {} as Theme;

const createTheme = (mode: PaletteMode, extendedTheme: Theme = defaultExtendedTheme) =>
  baseCreateTheme(
    deepmerge(
      {
        palette: {
          mode,
          primary: {
            main: '#15803d',
          },
          success: {
            main: '#00C853',
          },
        },
        components: {
          MuiCssBaseline: {
            styleOverrides: {
              ':root': {
                '--footer-height': '40px',
              },
            },
          },
        },
      },
      extendedTheme,
    ),
  );

export default createTheme;
