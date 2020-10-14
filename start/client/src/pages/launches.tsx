import React from "react";
import { RouteComponentProps } from "@reach/router";
import { gql, useQuery } from "@apollo/client";

import { LaunchTile, Header, Loading } from "../components";
import { Query, QueryLaunchArgs } from "../../schema.generated";

export const LAUNCH_TILE_DATA = gql`
  fragment LaunchTile on Launch {
    __typename
    id
    isBooked
    rocket {
      id
      name
    }
    mission {
      name
      missionPatch
    }
  }
`;

const GET_LAUNCHES = gql`
  query launchList($cursor: String) {
    launches(cursor: $cursor) {
      cursor
      has_more
      results {
        id
        is_booked
        rocket {
          id
          name
        }
        mission {
          name
          mission_patch
        }
      }
    }
  }
`;

interface LaunchesProps extends RouteComponentProps {}

const Launches: React.FC<LaunchesProps> = () => {
  const { data, loading, error } = useQuery<Query, QueryLaunchArgs>(GET_LAUNCHES);

  if (loading) return <Loading />;
  if (error) return <p>ERROR</p>;
  if (!data) return <p>Not found</p>;

  return (
    <>
      <Header />
      {data.launches.results.map((launch) => (
        <LaunchTile key={launch.id} launch={launch} />
      ))}
    </>
  );
};

export default Launches;
