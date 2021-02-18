using JuMP
using Clp
using IterTools

#=
Déclaration des données du problème
=#
n = 4
m = 3
U = 220
M = 15
c = [10,7,16,6]'
f = [40,45,32,55]'
beta = [1,0.6,0.1]'

d1 = [(0.5,0.00005),(1,0.00125),(2.5,0.0215),(3.5,0.2857),(5,0.3830),(6.5,0.2857),(7.5,0.0215),(9,0.00125),(9.5,0.00005)]
d2 = [(0,0.0013),(1.5,0.0215),(2.5,0.2857),(4,0.3830),(5.5,0.2857),(6.5,0.0215),(8,0.00125),(8.5,0.00005)]
d3 = [(0,0.0013),(0.5,0.0215),(1.5,0.2857),(3,0.3830),(4.5,0.2857),(5.5,0.0215),(7,0.00125),(7.5,0.00005)]
p = []
d = []

#=
Construction des 576 scénarios
=#
for a in product(d1,d2,d3)
    push!(p,a[1][2]* a[2][2] *a[3][2])
    push!(d,(a[1][1],a[2][1],a[3][1]))
    
end




function deterministic_model(d)
    model  = Model(Clp.Optimizer)


    #=
    Déclaration des variables de décision
    =#
    @variable(model, x[1:4],lower_bound = 0)
    @variable(model, y[1:3,1:4], lower_bound = 0)



    #=
    Déclaration des contraintes
    =#

    #Budgetary constraints
    @constraint(model,sum(x) <= M)
    @constraint(model,c*x <= U)

    #Max generation from a generator
    for j in 1:n 
        @constraint(model,sum(y[i,j] for i in 1:m) <= x[j])
    end

    #Demand satisfaction
    for i in 1:m
        @constraint(model,sum(y[i,j] for j in 1:n) == d[i])
    end


    #=
    Déclaration de l'objectif
    =#

    @objective(model,Min,c*x + beta*y*f')
    optimize!(model)
   
    return objective_value(model)
end


results = []
for demands in d
    push!(results,deterministic_model(demands))
end
println(results)
my name is Guillaume
