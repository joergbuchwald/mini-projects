
number_of_agents = 1500000

time_steps = 2000

mutable struct Agent
    infected::Bool
    immune::Bool
    inf_date::Int64
end

agents = Agent[]

function initialize!(agent_array::Array{Agent,1}, numofagents::Int64)
    append!(agent_array,[Agent(true,false,0)])
    for i in 1:numofagents
        append!(agent_array,[Agent(false,false,0)])
    end
    return agent_array
 end

function infect!(agent_array::Array{Agent,1}, time::Int64)
    for i in 1:length(agent_array)
        if agent_array[i].infected == true
            p = rand()
            if p < 0.05
                who = Int(floor(rand()*(1+length(agent_array))))
                if who == 0
                    who = length(agent_array)
                end
                if agent_array[who].immune == false
                    agent_array[who].infected = true
                    agent_array[who].inf_date = time
                end
            end
        end
    end
    return agent_array
end

function heal!(agent_array::Array{Agent,1}, time::Int64)
    for i in 1:length(agent_array)
        if agent_array[i].infected == true
            if (time - agent_array[i].inf_date) > 30
                p = rand()
                if p < 0.2
                    agent_array[i].infected = false
                    agent_array[i].immune = true
                end
            end
        end
    end
    return agent_array
end

function getnumofinfected(agent_array::Array{Agent,1})
    num_inf = 0
    num_imm = 0
    for i in 1:length(agent_array)
        if agent_array[i].infected == true
            num_inf = num_inf + 1
        end
        if agent_array[i].immune == true
            num_imm = num_imm + 1
        end
    end
    println(num_inf, " ", num_imm)
end

function time_loop!(agent_array::Array{Agent,1}, time_steps::Int64)
    for t in 1:time_steps
        infect!(agent_array, t)
        heal!(agent_array, t)
        getnumofinfected(agent_array)
    end
end


initialize!(agents,number_of_agents)
time_loop!(agents,time_steps)
