import { cleanup } from '@testing-library/react';
import { afterEach, vi } from 'vitest';

import { TEST_BASE_API } from 'test/constants';
import { swarmStateMock } from 'test/mocks/swarmState.mock';

global.window.templateArgs = swarmStateMock;
window.matchMedia = vi.fn().mockImplementation(() => ({
  matches: false,
}));

afterEach(() => {
  cleanup();
});

vi.mock('@reduxjs/toolkit/query/react', async () => {
  const actual = (await vi.importActual('@reduxjs/toolkit/query/react')) as { [key: string]: any };

  return { ...actual, fetchBaseQuery: () => actual.fetchBaseQuery({ baseUrl: TEST_BASE_API }) };
});