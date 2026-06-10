export const endpoints = {
  auth: {
    login: "/auth/login",
  },
  health: "/health",
  admin: {
    seed: "/admin/seed",
  },
  members: {
    list: (type?: string) => (type ? `/members?type=${type}` : "/members"),
    detail: (mid: number) => `/members/${mid}`,
    collection: "/members",
  },
  projects: {
    list: "/projects",
    detail: (pid: number) => `/projects/${pid}`,
    status: (pid: number) => `/projects/${pid}/status`,
    collection: "/projects",
  },
  grants: {
    members: (gid: number) => `/grants/${gid}/members`,
  },
  equipment: {
    list: "/equipment",
    detail: (eid: number) => `/equipment/${eid}`,
    activeUsers: (eid: number) => `/equipment/${eid}/active-users`,
    collection: "/equipment",
  },
  devices: {
    list: "/devices",
    detail: (did: number) => `/devices/${did}`,
    collection: "/devices",
  },
  uses: {
    list: "/uses",
    active: "/uses?active_only=true",
    detail: (mid: number, did: number, eid: number) => `/uses/${mid}/${did}/${eid}`,
    collection: "/uses",
  },
  reports: {
    topFundedProjects: "/reports/top-funded-projects",
    topMentorsByPublications: "/reports/top-mentors-by-publications",
    studentPublicationsByMajorYear: "/reports/student-publications-by-major-year",
    projectsEndedBefore: (date: string) =>
      `/reports/projects-ended-before?date=${date}`,
    topPublicationYears: "/reports/top-publication-years",
  },
};
