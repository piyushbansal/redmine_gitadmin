class GitadminController < ApplicationController
unloadable
helper :sort
include SortHelper
verify :method => :post, :only => :destroy

  def index
    sort_init 'Sno', 'asc'
    sort_update 'Sno' => "id",
    'Repository Name' => "#{Gitrepo.table_name}.reponame",
    'Created On' => "#{Gitrepo.table_name}.created_on"
    @project = Project.find(params[:project_id])
    @repos = Gitrepo.find(:all, :order => sort_clause)
  end
  
  def create 
    @project = Project.find(params[:project_id])
    # if !( @project && User.current.allowed_to?(:new_repo, @project))
    #   render_403
    #   return
    # end
    @repo = Gitrepo.new()
    if request.post?
      @repo.reponame = params[:gitrepo][:reponame].gsub(" ","-")
      @repo.lab_id = params[:project_id]
      @repo.description = params[:gitrepo][:description]
      response = @repo.manage('add',@repo.lab_id,@repo.reponame)
      flash.discard
      if response['status'] == 1
	@repo.created_on = Time.now.strftime("%Y-%m-%d %H:%M")
	@repo.save
	redirect_to :controller => 'gitadmin', :action => 'index', :project_id => @project
	flash[:notice] = "Creation successful"
	return
      else
	redirect_to :controller => 'gitadmin', :action => 'index', :project_id => @project
	flash[:error] = "Creation failed: " + response[:summary]
	return
      end
    end
  end
  def destroy
    @project = Project.find(params[:project_id])
    @repos = Gitrepo.find(:all)
    if request.post?
      @repos.each do |@repo|
        if params[:project_id] == @repo.lab_id
          if params[:repo] == @repo.reponame
            @repo.manage('discard',@repo.lab_id,@repo.reponame)
            @repo.delete
            redirect_to :controller => 'gitadmin', :action => 'index', :project_id => params[:project_id]
            return
          end
        end
      end
    end
  end
end
