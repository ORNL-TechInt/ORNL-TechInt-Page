  <div id="header">
    <div id="hbanner">
      <table id="header"><tr>
        <td id="logo"><img src="olcf-logo.png" alt="OLCF Logo"/></td>
        <td id="page_title"><h1>Technology Integration</h1></td>
      </tr></table>
    </div>

    <div class="navbar">
    <ul class="nav">
%ifeq(self.filetype, 'index')
      <li class="current_page" />
       <a class="current_page" href="index.html">About</a>
%else
      <li/>
       <a href="index.html">About</a>
%endif
%ifeq(self.filetype, 'projects')
      <li class="current_page" />
       <a class="current_page" href="projects.html">Thrust Areas</a>
%else
      <li/><a href="projects.html">Thrust Areas</a>
%endif
        <ul>
          <li/><a href="storage.html">File and Storage Systems</a>
          <li/><a href="nvm.html">Non-Volatile Memory</a>
          <li/><a href="data.html">Data Management</a>
          <li/><a href="networking.html">Networking</a>
          <li/><a href="architecture.html">Computer Architecture</a>
        </ul>
%ifeq(self.filetype, 'members')
      <li class="current_page" />
       <a class="current_page" href="members.html">Members</a>
%else
      <li/><a href="members.html">Members</a>
%endif
        <ul>
          <li/><a href="vazhkudai.html">Sudharshan Vazhkudai (group leader)</a>
          <li/><a href="mowery.html">Sonya Mowery (group secretary)</a>
          <li/><a href="atchley.html">Scotty Atchley</a>
          <li/><a href="barron.html">Tom Barron</a>
          <li/><a href="dillow.html">David Dillow</a>
          <li/><a href="fuller.html">Doug Fuller</a>
          <li/><a href="gunasekaran.html">Raghul Gunasekaran</a>
          <li/><a href="harney.html">John Harney</a>
          <li/><a href="kim.html">Youngjae Kim</a>
          <li/><a href="miller.html">Ross Miller</a>
          <li/><a href="oral.html">Sarp Oral</a>
          <li/><a href="sim.html">Hyogi Sim</a>
          <li/><a href="simmons.html">James Simmons</a>
          <li/><a href="smith.html">Brian Smith</a>
          <li/><a href="stansberry.html">Dale Stansberry</a>
          <li/><a href="steinert.html">Deryl Steinert</a>
          <li/><a href="cwang.html">Chao Wang</a>
          <li/><a href="fwang.html">Feiyi Wang</a>
          <li/><a href="white.html">Vicky White</a>
        </ul>
%ifeq(self.filetype, 'pub')
      <li class="current_page" />
       <a class="current_page" href="publications.html">Publications</a>
%else
      <li/><a href="publications.html">Publications</a>
%endif
        <ul>
          <li/><a href="publications.html#2013">2013</a>
          <li/><a href="publications.html#2012">2012</a>
          <li/><a href="publications.html#2011">2011</a>
          <li/><a href="publications.html#2010">2010</a>
          <li/><a href="publications.html#2009">2009 and earlier</a>
        </ul>
%ifeq(self.filetype, 'software')
      <li class="current_page" />
       <a class="current_page" href="software.html">Software</a>
%else
      <li/><a href="software.html">Software</a>
%endif
        <ul>
          <li/><a href="software.html#2012">2012</a>
          <li/><a href="software.html#2011">2011</a>
        </ul>
%ifeq(self.filetype, 'jobs')
      <li class="current_page" />
       <!-- <a class="current_page" href="jobs.html">Jobs</a> -->
       <a class="current_page" href="http://www.olcf.ornl.gov/about/careers/">Jobs</a>
%else
      <li/><!-- <a href="jobs.html">Jobs</a> -->
       <a href="http://www.olcf.ornl.gov/about/careers/">Jobs</a>
%endif
%ifeq(self.filetype, 'contact')
      <li class="current_page" />
       <a class="current_page" href="contact.html">Contact</a>
%else
      <li/><a href="contact.html">Contact Us</a>
%endif
      <li class="navfill"/>
    </ul>
    </div>
  </div>
